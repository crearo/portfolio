from flask import Flask
app = Flask(__name__)
@app.route('/')
def index():
	return "Yo, it's working! Here's a minor mod to see the diff to upload to heroku!"
if __name__ == "__main__":
	app.run()
