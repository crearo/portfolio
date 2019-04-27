import io
import json
import os

import datetime
import time
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)
fifa_learn = None

try:
    app.config['GA_TRACKING_ID'] = os.environ['GA_TRACKING_ID']
except:
    print('Tracking ID not set')

resume_pdf_link = 'https://drive.google.com/open?id=0B2BrrDjIiyvmcWp5T194cy00UmM'


@app.route('/')
def index():
    age = int((datetime.date.today() - datetime.date(1995, 4, 22)).days / 365)
    return render_template('home.html', age=age)


@app.route('/timeline')
def timeline():
    return render_template('timeline.html', resume_pdf_link=resume_pdf_link)


@app.route('/projects')
def projects():
    data = get_static_json("static/projects/projects.json")['projects']
    data.sort(key=order_projects_by_weight, reverse=True)

    tag = request.args.get('tags')
    if tag is not None:
        data = [project for project in data if tag.lower() in [project_tag.lower() for project_tag in project['tags']]]

    return render_template('projects.html', projects=data, tag=tag)


@app.route('/lifehacks/privacy-policy')
def lifehacks_privacy_policy():
    return render_template('lifehacks-privacy-policy.html')


@app.route('/dawebmail/privacy-policy')
def dawebmail_privacy_policy():
    return render_template('dawebmail-privacy-policy.html')


@app.route('/lifehacks/terms-and-conditions')
def lifehacks_disclaimer():
    return render_template('lifehacks-terms-and-conditions.html')


@app.route('/lifehacks/disclaimer')
def lifehacks_terms_and_conditions():
    return render_template('lifehacks-disclaimer.html')


@app.route('/mit-media-lab-application')
def media_lab_application():
    return render_template('mit-media-lab-application.html')


@app.route('/blog')
def blog():
    return redirect("http://bhardwajrish.blogspot.com/", code=302)


@app.route('/experiences')
def experiences():
    experiences = get_static_json("static/experiences/experiences.json")['experiences']
    experiences.sort(key=order_projects_by_weight, reverse=True)
    return render_template('projects.html', projects=experiences, tag=None)


def order_projects_by_weight(projects):
    try:
        return int(projects['weight'])
    except KeyError:
        return 0


@app.route('/projects/<title>')
def project(title):
    projects = get_static_json("static/projects/projects.json")['projects']
    experiences = get_static_json("static/experiences/experiences.json")['experiences']

    in_project = next((p for p in projects if p['link'] == title), None)
    in_exp = next((p for p in experiences if p['link'] == title), None)

    if in_project is None and in_exp is None:
        return render_template('404.html'), 404
    # fixme: choose the experience one for now, cuz I've done some shite hardcoding here.
    elif in_project is not None and in_exp is not None:
        selected = in_exp
    elif in_project is not None:
        selected = in_project
    else:
        selected = in_exp

    # load html if the json file doesn't contain a description
    if 'description' not in selected:
        path = "experiences" if in_exp is not None else "projects"
        selected['description'] = io.open(get_static_file(
            'static/%s/%s/%s.html' % (path, selected['link'], selected['link'])), "r", encoding="utf-8").read()
    return render_template('project.html', project=selected)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def get_static_file(path):
    site_root = os.path.realpath(os.path.dirname(__file__))
    return os.path.join(site_root, path)


def get_static_json(path):
    return json.load(open(get_static_file(path)))


"""
Specific URLs
"""


@app.route('/fifa-or-real')
def fifa_or_real():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        os.makedirs('./static/uploads/', exist_ok=True)
        file_name = 'upload-%s' % time.strftime("%Y-%m-%d-%H-%M-%S")
        f.save('./static/uploads/%s' % file_name)
        return redirect(url_for('predict_fifa', name=file_name))


@app.route('/predict-fifa')
def predict_fifa():
    import fastai.vision as fastai
    global fifa_learn

    name = request.args.get('name')
    path = './static/uploads/%s' % name
    print('------------------')
    print(path)
    if not os.path.exists(path):
        return "File doesn't exist, soz, go to the home page! %s" % path

    img = fastai.open_image(path)
    if fifa_learn is None:
        fifa_learn = fastai.load_learner('.', 'fifa.learn')
    pred_class, pred_idx, outputs = fifa_learn.predict(img)
    return render_template('fifa-or-real-predict.html', img=path, predict_class=pred_class, predict_confidence=outputs,
                           name=name)


if __name__ == "__main__":
    print("running py app")
    app.run(host="127.0.0.1", port=5000, debug=True)
