from flask import Flask, render_template, request, flash
from analyze import analyze_file
import os
app = Flask(__name__)
app.secret_key = 'wvjknsdvrbksvd609'

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/upload_document", methods=['POST'])
def upload_document():
	file = request.files['file']
	if file:
		file.save("example.txt")
		flash("Upload Successful!", "feedback")
	flash("No file chosen", "feedback")
	return render_template('index.html')


@app.route("/analyze", methods=['POST'])
def analyze():
	exclude_stop_words = request.form.get('exclude-stop-words')
	top_25 = analyze_file(exclude_stop_words)
	for pair in top_25:
		flash(pair, "analysis")
	return render_template('index.html')

if __name__ == "__main__":
	app.run()