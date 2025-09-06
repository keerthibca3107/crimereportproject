
from flask import Flask, render_template, redirect, url_for, request, flash, abort

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os
from flask import Flask, render_template, redirect, url_for, request, flash, abort
from models import db, User, CrimeReport

app = Flask(__name__)
app.config['SECRET_KEY'] = 'replace-with-a-secure-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crime_reports.db'
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Routes ---
@app.route('/')
def index():
    if os.path.exists('templates/index.html'):
        return render_template('index.html')
    return "Welcome to the Crime Reporting System Home Page!"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))
    return render_template('register.html') if os.path.exists('templates/register.html') else 'Register Page'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html') if os.path.exists('templates/login.html') else 'Login Page'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    reports = CrimeReport.query.all() if current_user.is_admin else CrimeReport.query.filter_by(user_id=current_user.id)
    return render_template('dashboard.html', reports=reports) if os.path.exists('templates/dashboard.html') else 'Dashboard Page'

@app.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        crime_type = request.form['crime_type']
        datetime = request.form['datetime']
        suspect_description = request.form.get('suspect_description', '')
        evidence = request.form.get('evidence', '')
        contact_info = request.form.get('contact_info', '')
        report = CrimeReport(
            title=title,
            description=description,
            location=location,
            crime_type=crime_type,
            datetime=datetime,
            suspect_description=suspect_description,
            evidence=evidence,
            contact_info=contact_info,
            user_id=current_user.id
        )
        db.session.add(report)
        db.session.commit()
        flash('Crime reported successfully!')
        return redirect(url_for('dashboard'))
    return render_template('report.html') if os.path.exists('templates/report.html') else 'Report Page'

# --- Admin Panel Routes ---
@app.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        abort(403)
    users = User.query.all()
    reports = CrimeReport.query.all()
    return render_template('admin_panel.html', users=users, reports=reports) if os.path.exists('templates/admin_panel.html') else 'Admin Panel Page'

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash('Cannot delete admin user!')
        return redirect(url_for('admin_panel'))
    db.session.delete(user)
    db.session.commit()
    flash('User deleted.')
    return redirect(url_for('admin_panel'))

@app.route('/admin/delete_report/<int:report_id>', methods=['POST'])
@login_required
def delete_report(report_id):
    if not current_user.is_admin:
        abort(403)
    report = CrimeReport.query.get_or_404(report_id)
    db.session.delete(report)
    db.session.commit()
    flash('Report deleted.')
    return redirect(url_for('admin_panel'))

@app.route('/admin/update_status/<int:report_id>', methods=['POST'])
@login_required
def update_status(report_id):
    if not current_user.is_admin:
        abort(403)
    report = CrimeReport.query.get_or_404(report_id)
    new_status = request.form.get('status')
    if new_status:
        report.status = new_status
        db.session.commit()
        flash('Report status updated.')
    return redirect(url_for('admin_panel'))

# --- Database Initialization ---
def initialize_database():
    with app.app_context():
        db.create_all()
        # Create default admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', is_admin=True)
            admin.set_password('admin123')  # Change this password after first login
            db.session.add(admin)
            db.session.commit()
        print('Database initialized and admin user created.')

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
