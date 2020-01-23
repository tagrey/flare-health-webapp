from flask import Flask, render_template, request, flash
from analyze import analyze_file, get_query
from flaskext.mysql import MySQL
import json

app = Flask(__name__)
app.secret_key = 'wvjknsdvrbksvd609'

mysql = MySQL()
mysql.init_app(app)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'nikki123'
app.config['MYSQL_DATABASE_DB'] = 'word_freq'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_SOCKET'] = None

@app.route("/")
def main():
	recent_analyses = get_recent_analyses()
	return render_template('index.html', data=get_recent_analyses())

@app.route("/upload_document", methods=['POST'])
def upload_document():
	recent_analyses = get_recent_analyses()
	file = request.files['file']
	if file:
		file.save("example.txt")
		flash("Upload Successful!", "feedback")
		with open("example.txt") as file_text:
			file_string = ''.join(file_text.readlines())
			flash(file_string, 'text_preview')
	else:
		flash("No file chosen", "feedback")
	return render_template('index.html', data=get_recent_analyses())


@app.route("/analyze", methods=['POST'])
def analyze():
	recent_analyses = get_recent_analyses()
	exclude_stop_words = request.form.get('exclude-stop-words') is not None
	top_25, query = analyze_file(exclude_stop_words)
	for pair in top_25:
		flash(pair, "analysis")
	make_query(query)
	return render_template('index.html', data=get_recent_analyses())

@app.route("/view_analysis", methods=['POST'])
def view_analysis():
	recent_analyses = get_recent_analyses()
	for pair in top_25:
		flash(pair, "analysis")
	return render_template('index.html', data=get_recent_analyses())

def make_query(query):
	cnx = mysql.connect()
	cursor = cnx.cursor()
	cursor.execute(query)
	cnx.commit()
	output = cursor.fetchall()
	cursor.close()
	cnx.close()
	return output

def get_recent_analyses():
	query = """SELECT SUBSTRING(original_text, 1, 15), exclude_stop_words FROM recent_analyses LIMIT 10"""
	return make_query(query)

if __name__ == "__main__":
	app.run()