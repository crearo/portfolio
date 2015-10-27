from flask import Flask, jsonify, request, make_response
from flask.ext.httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, redirect, url_for
from socket import gethostname
from flask.ext.wtf import Form 
from wtforms import TextField, TextAreaField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///me.db'
app.config['SECRET_KEY'] = 'HALO'

db = SQLAlchemy(app)
auth = HTTPBasicAuth()

class Music(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	m_name = db.Column(db.String)
	m_link = db.Column(db.String)
	m_text = db.Column(db.Text)
	m_date = db.Column(db.String)

	def __init__(self, m_name, m_link, m_text, m_date):
		self.m_name = m_name
		self.m_link = m_link
		self.m_text = m_text
		self.m_date = m_date

@app.route('/')
def home():
	color = 'blue'
	title = "Rishabh Bhardwaj"
	titleback = "RB"
	subtitle = "The fox crossed the way"
	subcontent = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
	return render_template('home.html',color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)

@app.route('/code')
def code():
	color = 'green'
	title = "Code"
	titleback = "C"
	subtitle = "The fox crossed the way"
	subcontent = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
	return render_template('home.html', color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)

@app.route('/weblog')
def weblog():
	color = 'dark'
	title = "WebLog"
	titleback = "W"
	subtitle = "A log of random musings, notes and things I find interesting"
	subcontent = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
	return render_template('home.html', color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)

@app.route('/music')
def music():

	songs = Music.query.all()

	color = 'red'
	title = "Music"
	titleback = "M"
	subtitle = "A Music Log"
	subcontent = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
	return render_template('music.html', songs = songs, color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)

@app.route('/contact')
def contact():
	color = 'orange'
	title = "Contact"
	titleback = "C"
	subtitle = "Let's get in touch"
	subcontent = "I love meeting new people and working on amazing things. If you'd like to work on a project with me, or get to know more about the work I do, do drop me a message. "
	return render_template('home.html', color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)