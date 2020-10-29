#!/usr/bin/env python
from flask import Flask, render_template, request, abort, url_for, redirect
import pymongo

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["db_deeper"]
# mydb.create_collection('deepers')
def get_themes():
    themes_l = []
    for i in mydb.deepers.find({}, {'_id': False}):
        themes_l.append(i)
    return themes_l 

PRODUCTS = get_themes()
 
@app.route('/')
@app.route('/home')
def home():
    PRODUCTS = get_themes()
    return render_template('home.html', products=PRODUCTS)
 
@app.route('/themes')
def themes():
    themes = list_themes()
    return render_template('themes.html', themes=themes)

    
@app.route('/add_video', methods=['POST'])
def add_video():
    data = get_themes()
    name = request.form.get("name")
    theme = request.form.get("theme")
    data = {
       'name': name,
       'theme': theme,
       'like': 0,
       'unlike': 0,
       'score': 0
    }
    mydb.deepers.insert_one(data)
    PRODUCTS.append(data)
    return redirect(url_for('home'))

@app.route('/like/<index>')
def like(index):
    data = get_themes()
    index = int(index)
    score = data[index]['like'] - (data[index]['unlike'] / 2)
    mydb.deepers.update(
      { "name": data[index]["name"] },
      { "$inc": { 'like': 1} })
    mydb.deepers.update(
      { "name": data[index]["name"] },
      { "$set": { 'score': score} })
    return redirect(url_for('home'))

@app.route('/unlike/<index>')
def unlike(index):
    data = get_themes()
    index = int(index)
    score = data[index].get('like') - (data[index].get('unlike') / 2)
    mydb.deepers.update(
      { "name": data[index]["name"] },
      { "$inc": { 'unlike': 1} })
    mydb.deepers.update(
      { "name": data[index]["name"] },
      { "$set": { 'score': score} })
    return redirect(url_for('home'))

def list_themes():
    high_themes = []
    mydoc = mydb.deepers.find({}).sort("score", -1)
    for i in mydoc:
        high_themes.append(i)
    return high_themes
