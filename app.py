import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Railway'dagi MONGO_URL o'zgaruvchisi orqali ulanish
MONGO_URI = os.environ.get("MONGO_URL")
client = MongoClient(MONGO_URI)
db = client['hikoyalar_db']
stories_collection = db['stories']

def to_cyrillic(text):
    """Lotin alifbosini Kirillga o'girish"""
    mapping = {
        "sh": "ш", "Sh": "Ш", "ch": "ч", "Ch": "Ч",
        "yo": "ё", "Yo": "Ё", "yu": "ю", "Yu": "Ю",
        "ya": "я", "Ya": "Я", "o'": "ў", "O'": "Ў",
        "g'": "ғ", "G'": "Ғ", "a": "а", "b": "б",
        "d": "д", "e": "е", "f": "ф", "g": "г",
        "h": "ҳ", "i": "и", "j": "ж", "k": "к",
        "l": "л", "m": "м", "n": "н", "o": "о",
        "p": "п", "q": "қ", "r": "р", "s": "с",
        "t": "т", "u": "у", "v": "в", "x": "х",
        "y": "й", "z": "з", "E": "Э", "e": "е"
    }
    res = text
    for lat, cyr in mapping.items():
        res = res.replace(lat, cyr)
    return res

@app.route('/')
def index():
    return redirect(url_for('admin'))

@app.route('/story/<story_id>')
def view_story(story_id):
    story_db = stories_collection.find_one({'_id': ObjectId(story_id)})
    if not story_db:
        return "Hikoya topilmadi", 404
    
    # Jinja2 uchun 'story' obyektini shakllantiramiz
    story = {
        "title_lat": story_db['title'],
        "title_cyr": to_cyrillic(story_db['title']),
        "content_lat": story_db['content'],
        "content_cyr": to_cyrillic(story_db['content'])
    }
    
    return render_template('story.html', story=story)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        stories_collection.insert_one({'title': title, 'content': content})
        return redirect(url_for('admin'))
    
    all_stories = list(stories_collection.find())
    return render_template('admin.html', stories=all_stories)

@app.route('/delete/<story_id>')
def delete_story(story_id):
    stories_collection.delete_one({'_id': ObjectId(story_id)})
    return redirect(url_for('admin'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
    
