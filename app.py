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
		flash("Upload Successful!")
		return render_template('index.html')

@app.route("/analyze", methods=['GET'])
def analyze():
	top_25 = analyze_file()
	flash(top_25)
	return render_template('index.html')

if __name__ == "__main__":
	app.run()