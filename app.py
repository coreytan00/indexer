from flask import Flask, render_template, url_for, request
import praw

def reddit(user_input, entries, category):
	reddit = praw.Reddit(client_id='aRbN-zQ8dpyF6A',
                     client_secret='_7ZBlE3dBMiKFbn9NgAZl-IkfSg',
                     user_agent='my_crawler')

	sub = reddit.subreddit(user_input)
	if category == "hot":
		submissions = sub.hot(limit=entries)
	elif category == "top":
		submissions = sub.top(limit=entries)
	elif category == "controversial":
		submissions = sub.controversial(limit=entries)
	return submissions

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
	return render_template("search.html")

@app.route('/search', methods=['POST'])
def search():
	user_input = request.form['index']
	words = user_input.split()
	return render_template("results.html", lst=words)

@app.route('/about')
def about():
	return 'not yet created!'

if __name__=="__main__":
	app.run(debug=True)

