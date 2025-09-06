
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(150), unique=True, nullable=False)
	password_hash = db.Column(db.String(128), nullable=False)
	is_admin = db.Column(db.Boolean, default=False)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

class CrimeReport(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	description = db.Column(db.Text, nullable=False)
	location = db.Column(db.String(200), nullable=False)
	crime_type = db.Column(db.String(100), nullable=False)
	datetime = db.Column(db.String(50), nullable=False)
	suspect_description = db.Column(db.Text)
	evidence = db.Column(db.Text)
	contact_info = db.Column(db.String(200))
	status = db.Column(db.String(50), default='Pending')
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', backref='reports')
	timestamp = db.Column(db.DateTime, server_default=db.func.now())
