from flask import Flask, render_template

app = Flask(__name__)

resume_pdf_link = 'https://drive.google.com/open?id=0B2BrrDjIiyvmcWp5T194cy00UmM'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/timeline')
def aboutme():
	return render_template('timeline.html', resume_pdf_link=resume_pdf_link)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    print("running py app")
    app.run(host="127.0.0.1", port=5000, debug=True)
