import json
import os

import datetime
from flask import Flask, render_template

app = Flask(__name__)

resume_pdf_link = 'https://drive.google.com/open?id=0B2BrrDjIiyvmcWp5T194cy00UmM'


@app.route('/')
def index():
    age = int((datetime.date.today() - datetime.date(1995, 4, 22)).days / 365)
    return render_template('home.html', age=age)


@app.route('/timeline')
def aboutme():
    return render_template('timeline.html', resume_pdf_link=resume_pdf_link)


@app.route('/projects')
def projects():
    return render_template('projects.html', projects=get_static_json("static/projects/projects.json")['projects'])


@app.route('/projects/<title>')
def project(title):
    selected = next((p for p in get_static_json("static/projects/projects.json")['projects'] if p['link'] == title),
                    None)
    if selected is None:
        return render_template('404.html'), 404
    return render_template('project.html', project=selected)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def get_static_json(path):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, path)
    return json.load(open(json_url))


if __name__ == "__main__":
    print("running py app")
    app.run(host="127.0.0.1", port=5000, debug=True)
