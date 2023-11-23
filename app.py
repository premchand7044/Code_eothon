from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func
import os
import traceback


######################### Setup #########################


# Initialize app
app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database object
db = SQLAlchemy(app)
migrate = Migrate(app, db)


######################### Model & Schema #########################


# Article Class/Model
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime(timezone=True), server_default=func.now())


######################### APIs #########################


# Create a article
@app.route('/article/create', methods=['POST'])
def create_article():
    try:
        article_dict = {
            'title' : request.json['title'],
            'author' : request.json['author'],
            'body' : request.json['body']
        }
        new_article = Article(**article_dict)
        db.session.add(new_article)
        db.session.commit()
        article_dict['id'] = new_article.id
        article_dict['pub_date'] = new_article.pub_date
        return jsonify(article_dict), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400


# Get all articles
@app.route('/article/all', methods=['GET'])
def get_all_articles():
    all_articles = Article.query.all()
    article_list = []
    for article in all_articles:
        article_list.append({
            'title' : article.title,
            'author' : article.author,
            'body' : article.body,
            'id': article.id,
            'pub_date': article.pub_date
        })
    return jsonify(article_list)


# Get single article
@app.route('/article/<id>', methods=['GET'])
def get_article(id):
    article = Article.query.get(id)
    if article == None:
        return jsonify({'error': f'no article found with the id {id}'}), 404
    article_dict = {
        'title' : article.title,
        'author' : article.author,
        'body' : article.body,
        'id': article.id,
        'pub_date': article.pub_date
    }
    return jsonify(article_dict)
@app.route('/article/search/title/<title>', methods=['GET'])
def search_title(title):
    all_articles = Article.query.filter(Article.title.contains(title))
    if not len(list(all_articles)):
        return jsonify({'error': f'no article found with the title {title}'}), 404
    article_list = []
    for article in all_articles:
        article_list.append({
            'title' : article.title,
            'author' : article.author,
            'body' : article.body,
            'id': article.id,
            'pub_date': article.pub_date
        })
    return jsonify(article_list)


# Update a article
@app.route('/article/update/<id>', methods=['PUT'])
def update_article(id):
    try:
        title = request.json['title']
        body = request.json['body']
        author = request.json['author']
        article = Article.query.get(id)
        if not article:
            return jsonify({'error': f'no article found with the id {id}'}), 404
        article.title = title
        article.body = body
        article.author = author
        db.session.commit()
        article_dict = {
            'title' : article.title,
            'author' : article.author,
            'body' : article.body,
            'id': article.id,
            'pub_date': article.pub_date
        }
        return jsonify(article_dict)
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400


# Delete article
@app.route('/article/delete/<id>', methods=['DELETE'])
def delete_article(id):
    article = Article.query.get(id)
    if not article:
        return jsonify({'error': f'no article found with id {id}'}), 404
    db.session.delete(article)
    db.session.commit()
    article_dict = {
        'title' : article.title,
        'author' : article.author,
        'body' : article.body,
        'id': article.id,
        'pub_date': article.pub_date
    }
    return jsonify(article_dict)



if __name__ == '__main__':
    app.run(debug=True, port=5000)