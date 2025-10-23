

# Flask web application for Lost and Found
from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'change_this_secret_key'
DATA_FILE = 'lost_found_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'lost': [], 'found': []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    data = load_data()
    lost_items = [dict(item, id=idx) for idx, item in enumerate(data['lost']) if item.get('status', 'open') == 'open'][-5:][::-1]
    found_items = [dict(item, id=idx) for idx, item in enumerate(data['found']) if item.get('status', 'open') == 'open'][-5:][::-1]
    return render_template('index.html', lost_items=lost_items, found_items=found_items)

@app.route('/add/<category>', methods=['GET', 'POST'])
def add_item(category):
    if category not in ['lost', 'found']:
        return 'Invalid category', 400
    if request.method == 'POST':
        item = {
            'name': request.form['name'],
            'description': request.form['description'],
            'date': request.form['date'],
            'location': request.form['location'],
            'contact': request.form['contact'],
            'status': 'open'
        }
        data = load_data()
        data[category].append(item)
        save_data(data)
        flash(f'{category.capitalize()} item added successfully!')
        return redirect(url_for('index'))
    return render_template('add_item.html', category=category)

@app.route('/search')
def search():
    query = request.args.get('q', '').strip().lower()
    results = None
    if query:
        data = load_data()
        results = []
        for category in ['lost', 'found']:
            for item in data[category]:
                if (query in item['name'].lower() or query in item['description'].lower()) and item.get('status', 'open') == 'open':
                    item_copy = item.copy()
                    item_copy['category'] = category
                    results.append(item_copy)
    return render_template('search.html', results=results)

@app.route('/resolve/<category>/<int:item_id>', methods=['POST'])
def resolve_item(category, item_id):
    if category not in ['lost', 'found']:
        return 'Invalid category', 400
    data = load_data()
    try:
        data[category][item_id]['status'] = 'resolved'
        save_data(data)
        flash(f'{category.capitalize()} item marked as resolved!')
    except (IndexError, KeyError):
        flash('Item not found.', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
