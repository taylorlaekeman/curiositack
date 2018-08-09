from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.Text, unique=True, nullable=False)
	password_hash = db.Column(db.Text, nullable=False)
	post = db.relationship('Post')

	def __repr__(self):
		return '<User {}>'.format(self.email)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	account = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	tack = db.Column(db.Integer, db.ForeignKey('tacks.id'), nullable=False)

class Tack(db.Model):
	__tablename__ = 'tacks'
	id = db.Column(db.Integer, primary_key=True)
	link = db.Column(db.Text, unique=True, nullable=False)
	post = db.relationship('Post')

	def __repr__(self):
		return '<Tack {}: {}>'.format(self.id, self.link)
