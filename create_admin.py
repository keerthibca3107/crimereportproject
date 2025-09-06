from app import app, db
from models import User

def create_admin():
    with app.app_context():
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', is_admin=True)
            admin.set_password('admin123')  # Change this password after first login
            db.session.add(admin)
            db.session.commit()
            print('Admin user created.')
        else:
            print('Admin user already exists.')

if __name__ == '__main__':
    create_admin()
