from flask import Flask, jsonify, request, make_response, Response, flash
from flask.ext.httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, redirect, url_for
import random, time
from socket import gethostname
from flask.ext.wtf import Form 
from wtforms import StringField, TextField, TextAreaField, SubmitField, IntegerField
from wtforms import validators
from functools import wraps
import re, json
from flask.ext.mail import Message, Mail

mail = Mail()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///me5.db'
app.config['SECRET_KEY'] = '!ntOthEwilD'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'androrish@gmail.com'
app.config["MAIL_PASSWORD"] = '!ntOthEwilD'

db = SQLAlchemy(app)
auth = HTTPBasicAuth()
mail.init_app(app)

current_time_in_millis = lambda: int(round(time.time() * 1000))

def check_auth(username, password):
	return username == 'rish' and password == 'kidinjp2'

def authenticate():
	return Response('Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth or not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated

class Music(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	m_name = db.Column(db.String)
	m_link = db.Column(db.String)
	m_text = db.Column(db.Text)
	m_date = db.Column(db.String)
	m_weight = db.Column(db.Integer)

	def __init__(self, m_name, m_link, m_text, m_date, m_weight):
		self.m_name = m_name
		self.m_link = m_link
		self.m_text = m_text
		self.m_date = m_date
		self.m_weight = m_weight

class MusicForm(Form):
	mf_name = StringField('mf_name', validators=[validators.required()])
	mf_link = StringField('mf_link', validators=[validators.required()])
	mf_text = TextAreaField('mf_text', validators=[validators.required(),validators.optional()])
	mf_weight = IntegerField('mf_weight', validators=[validators.required()])

class ContactForm(Form):
	c_name = StringField('c_name', validators=[validators.required()])
	c_email = StringField('c_email', validators=[validators.required()])
	c_msg = TextAreaField('c_msg', validators=[validators.required()])

@app.route("/")
def root():
	return redirect(url_for('home'))

@app.route('/home')
def home():
	color = 'blue'
	title = "Rishabh Bhardwaj"
	titleback = "RB"
	subtitle = "Coder | Traveler | Athlete | Developer"
	#subcontent = "Hi there! Polyglot full-stack developer? That's the aim. Steadily reaching there. I'm pursuing my undergrad degree in CS at DA-IICT, and am in my Junior year. I love keeping myself super busy, making things people will use, running, and playing football. Oh and FIFA too :D"
	#subcontent = "Me? 5+ apps on Google Plays, developer, creative thinker, problem solver. Undergrad in CS at DA-IICT- Junior year. I love keeping myself super busy, making things people will use, running, and playing football. FIFA 14, labradors, traveling, meeting new people :D"
	subcontent = 'Read More<a href = "/aboutme" class="aref">About Me</a> Here'
	return render_template('home.html',color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)

@app.route('/portfolio')
def portfolio():

	projectsFile = app.open_resource('static/projects.json')
	projects = json.loads(projectsFile.read())['projects']
	
	color = 'blue'
	title = "Portfolio"
	titleback = "CV"
	subtitle = "A log of my perpetually increasing list of projects."
	subcontent = "I could have made a fancy resume here, listing my work-exs, education history, but that's boring and we've got LinkedIn for that. This is a log of projects I've worked on indepenently, with organizations, and in my university."
	return render_template('portfolio.html', projects = projects, color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)

@app.route('/code')
def code():
	color = 'green'
	title = "Code"
	titleback = "C"
	subtitle = "I love making things. And code allows me to do so in the laziest way possible. Laptop, bed, and some coffee."
	subcontent = "Coding has become a major part of my life. Majorly because code just makes life so much easier. Whether it's a mobile app, an arduino based room locker, or a simple shell script to boot your laptop faster. Oh, and partly because this is the only way I see myself making money to fund my bucketlist."
	return render_template('code.html', color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)

@app.route('/weblog', defaults={'weblogno':None})
@app.route('/weblog/<weblogno>')
def weblog_ind(weblogno):

	return redirect("http://bhardwajrish.blogspot.in/");

	weblogs = None

	if weblogno == None:
		#weblogs = Weblog.query.all()
		weblogsFile = app.open_resource('static/weblogs.json')
		weblogs = json.loads(weblogsFile.read())['weblogs']

	elif weblogno == 'random-list':
		weblogsFile = app.open_resource('static/weblogs.json')
		weblogs = json.loads(weblogsFile.read())['weblogs']
		random.shuffle(weblogs, random.random)

	elif weblogno == 'favorites':
		weblogs = []
		weblogsFile = app.open_resource('static/weblogs.json')
		weblogs_temp = json.loads(weblogsFile.read())['weblogs']
		for w in weblogs_temp :
			if w['w_weight'] is 1 :
				weblogs.append(w)

	if weblogs is not None:
		# DISPLAY WEBLOG PAGE WITH SELECTED FILTERS
		color = 'dark'
		title = "WebLog"
		titleback = "W"
		subtitle = "A log of random musings, notes and things I find interesting"
		subcontent = "Most of my notes are short paragraphs (and not super long blogs that no one reads) on ideas and thoughts that cross my mind, fun observations about people and my surroundings, songs, travel, and sport."
		return render_template('weblog.html', weblogs = weblogs, color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)		

	else:
		# DISPLAY INDIVIDUAL WEBLOG
		color = 'green'
		title = "WebLog"
		titleback = "W"
		subtitle = "A log of random musings, notes and things I find interesting"
		subcontent = "Most of my notes are short paragraphs (and not super long blogs that no one reads) on ideas and thoughts that cross my mind, fun observations about people and my surroundings, songs, travel, and sport."
		#weblog = Weblog.query.filter_by(id = weblogno).first()
		weblogsFile = app.open_resource('static/weblogs.json')
		weblogs = json.loads(weblogsFile.read())['weblogs']
		for w in weblogs:
			if w['id'] is int(weblogno):
				return render_template('weblog_ind.html', weblog = w, color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)	
		return redirect(url_for('page_not_found'))

@app.route('/add/<addwhat>', methods = ['POST', 'GET'])
@requires_auth
def addContent(addwhat):
	if addwhat == 'song' or addwhat == 'music':
		form = MusicForm()
		if request.method == 'POST':
			if form.validate_on_submit():
				music = Music(form.mf_name.data,form.mf_link.data,form.mf_text.data, current_time_in_millis(), form.mf_weight.data)
				db.session.add(music)
				db.session.commit()
				return redirect(url_for('music', link = None))
			else :
				return 'invalid details entered'
		else:
			return render_template("music_create.html", form = form)

@app.route('/music', defaults={'link':None}, methods = ['GET', 'POST'])
@app.route('/music/<link>', methods = ['GET', 'POST'])
def music(link):
	songs = None
	if link == None:
		songs = Music.query.all()
	elif link == 'random-list':
		songs = Music.query.all()
		random.shuffle(songs, random.random)
	elif link == 'favorites':
		songs = Music.query.filter_by(m_weight = 1).all()
	
	if songs is not None:
		color = 'red'
		title = "Music"
		titleback = "M"
		subtitle = "A Music Log"
		subcontent = "Without songs, you simply cannot spend half your day on a laptop writing code. So here's a throwback to the songs I love. - Some I am currently listening to, some I had a phase of, and some that'll remain in my playlist even when Im 70."
		return render_template('music.html', 	songs = songs, color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)

@app.route('/contact', methods = ['POST', 'GET'])
def contact():
	form = ContactForm()
	color = 'orange'
	title = "Contact"
	titleback = "C"
	subtitle = "Let's get in touch"
	subcontent = "I love meeting new people and working on amazing things. If you'd like to work on a project with me, or get to know more about the work I do, do drop me a message. "

	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('contact.html', form = form, color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)
		else:
			msg = Message("Great Website Man!", sender='androrish@gmail.com', recipients=['bhardwaj.rish@gmail.com'])
			msg.body = """ From: %s <%s> %s """ % (form.c_name.data, form.c_email.data, form.c_msg.data)
			mail.send(msg)
			form = ContactForm()
			return render_template('contact.html', success=True, form = form, color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)
	
	return render_template('contact.html', form = form, color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)

@app.route('/aboutme')
def aboutme():
	return render_template('aboutme.html')	

@app.route('/places')
def places():
	return render_template('places.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', color = 'yellow', title = "Hold On!", titleback = "404", subtitle = "This page does not exist."), 404

if __name__ == '__main__':
	db.create_all()
	#app.run(host="192.168.150.1",port=8080, debug=True)
	app.run(debug=True)