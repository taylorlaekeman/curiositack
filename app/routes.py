from app import app, db
from app.models import Post, Tack, User
from app.forms import AddTackForm, LoginForm, RegistrationForm
from flask import redirect, render_template, url_for
from flask_login import current_user, login_user

@app.route('/', methods=['GET', 'POST'])
def index():
	if current_user.is_anonymous:
		return redirect(url_for('login'))
	tacks = Tack.query.all()
	form = AddTackForm()
	if form.validate_on_submit():
		add_tack(form)
		return redirect(url_for('index'))
	return render_template('board.html', user='me', tacks=tacks, form=form)

def add_tack(form):
	post = Post()
	tack = Tack.query.filter_by(link=form.link.data).first()
	if tack is None:
		tack = Tack(link=form.link.data)
	current_user.post.append(post)
	tack.post.append(post)
	db.session.add(tack)
	db.session.add(post)
	db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data.lower()).first()
		if user is not None and user.check_password(form.password.data):
			login_user(user)
			return redirect(url_for('index'))
	return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		register_user(form.email.data.lower(), form.password.data)
		login_user(User.query.filter_by(email=form.email.data.lower()).first())
		return redirect(url_for('index'))
	return render_template('register.html', form=form)

def register_user(email, password):
	user = User(email=email)
	user.set_password(password)
	db.session.add(user)
	db.session.commit()
