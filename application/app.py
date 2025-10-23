from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_user(email):
    data = load_data()
    for user in data['users']:
        if user['email'] == email:
            return user
    return None

def is_admin():
    return session.get('user_email') == 'sandaleefernando1@gmail.com'

def is_logged_in():
    return 'user_email' in session

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user(email)
        if user and user['password'] == password:
            session['user_email'] = user['email']
            session['user_role'] = user['role']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        return redirect(url_for('login'))
    data = load_data()
    user = get_user(session['user_email'])
    # Only show cupboards user is allowed to access
    allowed_storage = []
    for c in data['storage']:
        if c.get('secured'):
            if is_admin() or user['role'] == 'secretary':
                allowed_storage.append(c)
        else:
            allowed_storage.append(c)
    return render_template('dashboard.html', user=user, storage=allowed_storage, is_admin=is_admin())

# File action: Check Out
@app.route('/checkout/<int:cab_id>/<int:drawer_idx>/<int:file_idx>', methods=['POST'])
def checkout_file(cab_id, drawer_idx, file_idx):
    if not is_logged_in():
        return redirect(url_for('login'))
    data = load_data()
    user_email = session['user_email']
    user = get_user(user_email)
    expected_return = request.form.get('expected_return')
    cupboard = next((c for c in data['storage'] if c['id'] == cab_id), None)
    if not cupboard:
        flash('Cupboard not found.', 'danger')
        return redirect(url_for('dashboard'))
    if cupboard.get('secured') and not (is_admin() or user['role'] == 'secretary'):
        flash('You do not have permission to access this cupboard.', 'danger')
        return redirect(url_for('dashboard'))
    try:
        file = cupboard['drawers'][drawer_idx]['files'][file_idx]
        if file.get('status') == 'checked_out':
            flash('File already checked out.', 'warning')
        else:
            file['status'] = 'checked_out'
            file.setdefault('history', []).append({
                'action': 'checked_out',
                'by': user_email,
                'date': request.form.get('date', ''),
                'expected_return': expected_return
            })
            save_data(data)
            flash('File checked out.', 'success')
    except Exception as e:
        flash('Error checking out file.', 'danger')
    return redirect(url_for('dashboard'))

# File action: Return
@app.route('/return/<int:cab_id>/<int:drawer_idx>/<int:file_idx>', methods=['POST'])
def return_file(cab_id, drawer_idx, file_idx):
    if not is_logged_in():
        return redirect(url_for('login'))
    data = load_data()
    user_email = session['user_email']
    user = get_user(user_email)
    cupboard = next((c for c in data['storage'] if c['id'] == cab_id), None)
    if not cupboard:
        flash('Cupboard not found.', 'danger')
        return redirect(url_for('dashboard'))
    if cupboard.get('secured') and not (is_admin() or user['role'] == 'secretary'):
        flash('You do not have permission to access this cupboard.', 'danger')
        return redirect(url_for('dashboard'))
    try:
        file = cupboard['drawers'][drawer_idx]['files'][file_idx]
        if file.get('status') != 'checked_out':
            flash('File is not checked out.', 'warning')
        else:
            file['status'] = 'available'
            file.setdefault('history', []).append({
                'action': 'returned',
                'by': user_email,
                'date': request.form.get('date', '')
            })
            save_data(data)
            flash('File returned.', 'success')
    except Exception as e:
        flash('Error returning file.', 'danger')
    return redirect(url_for('dashboard'))

# File action: Handover
@app.route('/handover/<int:cab_id>/<int:drawer_idx>/<int:file_idx>', methods=['POST'])
def handover_file(cab_id, drawer_idx, file_idx):
    if not is_logged_in():
        return redirect(url_for('login'))
    data = load_data()
    user_email = session['user_email']
    user = get_user(user_email)
    to_user = request.form.get('to_user')
    handover_note = request.form.get('handover_note')
    cupboard = next((c for c in data['storage'] if c['id'] == cab_id), None)
    if not cupboard:
        flash('Cupboard not found.', 'danger')
        return redirect(url_for('dashboard'))
    if cupboard.get('secured') and not (is_admin() or user['role'] == 'secretary'):
        flash('You do not have permission to access this cupboard.', 'danger')
        return redirect(url_for('dashboard'))
    try:
        file = cupboard['drawers'][drawer_idx]['files'][file_idx]
        file.setdefault('history', []).append({
            'action': 'handover',
            'by': user_email,
            'to': to_user,
            'note': handover_note,
            'date': request.form.get('date', '')
        })
        file['status'] = 'handed_over'
        save_data(data)
        flash('File handed over.', 'success')
    except Exception as e:
        flash('Error handing over file.', 'danger')
    return redirect(url_for('dashboard'))


# File registration (add new file)
@app.route('/register', methods=['GET', 'POST'])
def register_file():
    if not is_logged_in():
        return redirect(url_for('login'))
    data = load_data()
    user = get_user(session['user_email'])
    suggestion = None
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        created = request.form['created']
        keywords = request.form['keywords']
        cupboard_id = int(request.form['cupboard'])
        drawer_name = request.form['drawer']
        # Find cupboard and drawer
        cupboard = next((c for c in data['storage'] if c['id'] == cupboard_id), None)
        if not cupboard:
            flash('Cupboard not found.', 'danger')
            return redirect(url_for('register_file'))
        drawer = next((d for d in cupboard['drawers'] if d['name'] == drawer_name), None)
        if not drawer:
            # Create drawer if not exists
            drawer = {'name': drawer_name, 'files': []}
            cupboard['drawers'].append(drawer)
        new_file = {
            'title': title,
            'category': category,
            'created': created,
            'keywords': keywords,
            'status': 'available',
            'history': [{
                'action': 'created',
                'by': user['email'],
                'date': created
            }]
        }
        drawer['files'].append(new_file)
        save_data(data)
        flash('File registered and stored successfully!', 'success')
        return redirect(url_for('dashboard'))
    # Suggest optimal spot: find drawer with fewest files in selected cupboard
    if request.method == 'GET' and request.args.get('cupboard'):
        cupboard_id = int(request.args['cupboard'])
        cupboard = next((c for c in data['storage'] if c['id'] == cupboard_id), None)
        if cupboard and cupboard['drawers']:
            suggestion = min(cupboard['drawers'], key=lambda d: len(d['files']))['name']
    return render_template('register.html', user=user, storage=data['storage'], suggestion=suggestion)

if __name__ == '__main__':
    app.run(debug=True)
