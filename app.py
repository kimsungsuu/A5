from flask import Flask, render_template, request, jsonify, redirect
app = Flask(__name__)

from bson.objectid import ObjectId

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.awfowzp.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/movies/new", methods=["GET"])
def get_write():

   return render_template('write.html')

@app.route("/movies/new", methods=["POST"])
def post_write():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']

    
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    ogtitle = soup.select_one('meta[property="og:title"]')['content']
    ogimage = soup.select_one('meta[property="og:image"]')['content']
    ogdesc = soup.select_one('meta[property="og:description"]')['content']
    
    doc = {
       'title' : ogtitle,
       'desc' : ogdesc,
       'image' : ogimage,
       'url' : url_receive,
       'comment' : comment_receive,
       'star' : star_receive,
    }
    
    db.movies.insert_one(doc)

    return redirect('/')

@app.route("/movie", methods=["GET"])
def movie_get():
    all_movies = list(db.movies.find({},{'_id':True, 'title':True, 'desc':True, 'image':True, 'star':True, 'comment':True}))
    
    # ObjectId 값을 String 형식으로 변환
    for movie in all_movies:
        movie['_id'] = str(movie['_id'])
        
    return jsonify({'result':all_movies})
 

@app.route("/view/<id>", methods=["GET"])
def one_find_movie(id):
    
    find_movie = db.movies.find_one({"_id": ObjectId(id)})
    find_movie['_id'] = str(find_movie['_id'])

    return jsonify({'result':find_movie})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)