from flask import Flask, jsonify, request, make_response
from flask.ext.httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, redirect, url_for
import random
from socket import gethostname
from flask.ext.wtf import Form 
from wtforms import TextField, TextAreaField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///me3.db'
app.config['SECRET_KEY'] = 'HALO'

db = SQLAlchemy(app)
auth = HTTPBasicAuth()

class Music(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	m_name = db.Column(db.String)
	# m_artist = db.Column(db.String)
	m_link = db.Column(db.String)
	m_text = db.Column(db.Text)
	m_date = db.Column(db.String)

	def __init__(self, m_name, m_link, m_text, m_date):
		self.m_name = m_name
		self.m_link = m_link
		self.m_text = m_text
		self.m_date = m_date

class Weblog(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	w_title = db.Column(db.String)
	w_link =  db.Column(db.String)
	w_content = db.Column(db.String)
	w_dateposted = db.Column(db.String)
	w_category = db.Column(db.String)
	w_weight = db.Column(db.Integer)

	def __init__(self, w_title, w_link, w_content, w_dateposted, w_category,w_weight):
		self.w_title = w_title
		self.w_link = w_link
		self.w_content = w_content
		self.w_dateposted = w_dateposted
		self.w_category = w_category
		self.w_weight = w_weight

class Job(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	j_company =  db.Column(db.String)
	j_title =  db.Column(db.String)
	j_startdate =  db.Column(db.String)
	j_enddate =  db.Column(db.String)
	j_duration =  db.Column(db.String)
	j_description =  db.Column(db.String)
	j_link =  db.Column(db.String)

	def __init__(self, j_company,j_title,j_startdate,j_enddate,j_duration,j_description,j_link):
		self.j_company = j_company
		self.j_title = j_title
		self.j_startdate = j_startdate
		self.j_enddate = j_enddate
		self.j_duration = j_duration
		self.j_description = j_description
		self.j_link = j_link

class Eduaction(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	e_name =  db.Column(db.String)
	e_degree =  db.Column(db.String)
	e_major =  db.Column(db.String)
	e_description =  db.Column(db.String)
	e_startdate =  db.Column(db.String)
	e_enddate =  db.Column(db.String)
	e_link =  db.Column(db.String)

	def __init__(self,e_name, e_degree,e_major,e_description,e_startdate,e_enddate,	e_link):
		self.e_name = e_name
		self.e_degree = e_degree
		self.e_major = e_major
		self.e_description = e_description
		self.e_startdate = e_startdate
		self.e_enddate = e_enddate
		self.e_link = e_link


class Project(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	p_name = db.Column(db.String)
	p_category = db.Column(db.String)
	p_date = db.Column(db.String)
	p_short = db.Column(db.String)
	p_description = db.Column(db.String)
	p_link = db.Column(db.String)
	p_image1 = db.Column(db.String)
	p_image2 = db.Column(db.String)
	p_image3 = db.Column(db.String)
	p_weight = db.Column(db.Integer)
	p_status = db.Column(db.String)
	p_tech_used = db.Column(db.String)

	def __init__(self, p_name,p_category,p_date,p_short,p_description,p_link,p_image1,p_image2,p_image3,p_weight, p_status, p_tech_used):
		self.p_name = p_name
		self.p_category = p_category
		self.p_date = p_date
		self.p_short = p_short
		self.p_description = p_description
		self.p_link = p_link
		self.p_image1 = p_image1
		self.p_image2 = p_image2
		self.p_image3 = p_image3
		self.p_weight = p_weight
		self.p_status = p_status
		self.p_tech_used = p_tech_used

@app.route("/")
def root():
	return redirect(url_for('home'))

@app.route('/home')
def home():
	color = 'blue'
	title = "Rishabh Bhardwaj"
	titleback = "RB"
	subtitle = "Coder | Maker | Athlete | Developer"
	subcontent = "Hi there! Polyglot full-stack developer? That's the aim. Steadily reaching there. I'm pursuing my undergrad degree in CS at DA-IICT, and am in my Junior year. I love keeping myself super busy, making things people will use, running, and playing football. Oh and FIFA too :D"
	return render_template('home.html',color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)

@app.route('/portfolio')
def portfolio():
	jobs = Job.query.all()
	edus = Eduaction.query.all()
	projects = Project.query.all()

	color = 'blue'
	title = "Portfolio"
	titleback = "CV"
	subtitle = "A log of my perpetually increasing list of projects."
	subcontent = "I could have made a fancy resume here, listing my work-exs, education history, but that's boring and we've got LinkedIn for that. This is a log of projects I've worked on indepenently, with organizations, and in my university."
	return render_template('portfolio.html', projects = projects, jobs = jobs, edus = edus, color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)


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

	weblogs = None

	if weblogno == None:
		weblogs = Weblog.query.all()

	elif weblogno == 'random-list':
		weblogs = Weblog.query.all()
		random.shuffle(weblogs, random.random)

	elif weblogno == 'favorites':
		weblogs = Weblog.query.filter_by(w_weight = 1).all()
	
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
		weblog = Weblog.query.filter_by(id = weblogno).first()
		if weblog != None:
			return render_template('weblog_ind.html', weblog = weblog, color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)
		else :
			return '404'

@app.route('/music', defaults={'link':None})
@app.route('/music/<link>')
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

@app.route('/contact')
def contact():
	color = 'orange'
	title = "Contact"
	titleback = "C"
	subtitle = "Let's get in touch"
	subcontent = "I love meeting new people and working on amazing things. If you'd like to work on a project with me, or get to know more about the work I do, do drop me a message. "
	return render_template('contact.html', color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)