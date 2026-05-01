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

@app.route('/')
def index():
    # Asosiy sahifaga kirganda admin panelga yo'naltiramiz yoki hikoyalar ro'yxatiga
    return redirect(url_for('admin'))

@app.route('/story/<story_id>')
def view_story(story_id):
    story = stories_collection.find_one({'_id': ObjectId(story_id)})
    if not story:
        return "Hikoya topilmadi", 404
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
    
