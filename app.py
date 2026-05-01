import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Railway'dan MongoDB havolasini olish (environment variable)
MONGO_URI = os.environ.get("MONGO_URL", "mongodb://localhost:27017/") 
client = MongoClient(MONGO_URI)

# Baza va Kolleksiyani yaratish/ulash
db = client['hikoyalar_db']
stories_collection = db['stories']

@app.route('/')
def index():
    return redirect(url_for('admin'))

# HIKOYA O'QISH SAHIFASI
@app.route('/story/<story_id>')
def view_story(story_id):
    try:
        story = stories_collection.find_one({'_id': ObjectId(story_id)})
    except:
        return "Noto'g'ri ID formati", 400

    if not story:
        return "Hikoya topilmadi", 404
        
    return render_template('story.html', story=story, story_id=str(story['_id']))

# ADMIN PANEL (Qo'shish va Ko'rish)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        # Bazaga saqlash
        stories_collection.insert_one({
            'title': title,
            'content': content
        })
        return redirect(url_for('admin'))
    
    # Barcha hikoyalarni bazadan olish
    all_stories = list(stories_collection.find())
    return render_template('admin.html', stories=all_stories)

# HIKOYANI TAHRIRLASH
@app.route('/edit/<story_id>', methods=['GET', 'POST'])
def edit_story(story_id):
    if request.method == 'POST':
        new_title = request.form.get('title')
        new_content = request.form.get('content')
        
        # Bazada yangilash
        stories_collection.update_one(
            {'_id': ObjectId(story_id)},
            {'$set': {'title': new_title, 'content': new_content}}
        )
        return redirect(url_for('admin'))
        
    # Tahrirlash sahifasiga eski ma'lumotlarni yuborish
    story = stories_collection.find_one({'_id': ObjectId(story_id)})
    return render_template('edit.html', story=story)

# HIKOYANI O'CHIRISH
@app.route('/delete/<story_id>')
def delete_story(story_id):
    stories_collection.delete_one({'_id': ObjectId(story_id)})
    return redirect(url_for('admin'))

if __name__ == '__main__':
    # Railway o'z portini beradi, yo'qsa 5000 da ishlaydi
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
      
