from flask import Flask, render_template, request, flash
from analyze import analyze_file, get_query
from flaskext.mysql import MySQL
import json
from ast import literal_eval

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
	return render_template('index.html', data=get_recent_analyses())

@app.route("/upload_document", methods=['POST'])
def upload_document():
	#endlpoint handling file upload
	recent_analyses = get_recent_analyses()
	file = request.files['file']
	if file:
		file.save("tmp.txt") #use this as a temp file
		flash("Upload Successful!", "feedback")
		with open("tmp.txt") as file_text:
			file_string = ''.join(file_text.readlines())
			flash(file_string, 'text_preview')
	else:
		flash("No file chosen", "feedback")
	return render_template('index.html', data=get_recent_analyses())


@app.route("/analyze", methods=['POST'])
def analyze():
	#endpoint handling analysis of a file
	recent_analyses = get_recent_analyses()
	exclude_stop_words = request.form.get('exclude-stop-words') is not None
	top_25, query = analyze_file(exclude_stop_words)
	for pair in top_25:
		flash(pair, "analysis")
	make_query(query)
	return render_template('index.html', data=get_recent_analyses())

@app.route("/view_analysis", methods=['POST'])
def view_analysis():
	#endpoint handling viewing the results of an old analysis
	recent_analyses = get_recent_analyses()
	most_recent_analysis = str(recent_analyses[0])
	most_recent_top_25 = literal_eval(literal_eval(most_recent_analysis)[2])
	top_25 = request.form.get('analysis_details')
	top_25 = literal_eval(literal_eval(top_25)[2])
	for pair in top_25:
		flash(pair, "old_analysis")
	for pair in most_recent_top_25: #need to rerender the most recent analysis we did on the left
		flash(pair, "analysis")
	return render_template('index.html', data=get_recent_analyses())

def make_query(query):
	#execute a SQL query
	cnx = mysql.connect()
	cursor = cnx.cursor()
	cursor.execute(query)
	cnx.commit()
	output = cursor.fetchall()
	cursor.close()
	cnx.close()
	return output

def get_recent_analyses():
	#always need to query the most recent analyses to pass to index.html
	query = """SELECT SUBSTRING(original_text, 1, 15), exclude_stop_words, word_frequencies FROM recent_analyses ORDER BY date DESC LIMIT 10"""
	return make_query(query)

if __name__ == "__main__":
	app.run()