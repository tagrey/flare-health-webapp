from flask import Flask, render_template, request, flash
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
	frequencies = dict()
	with open('example.txt') as text_file:
		line = text_file.readline()
		while line:
			words = line.split(' ')
			for word in words:
				word = word.replace('\n', '')
				if word not in frequencies:
					frequencies[word] = 0
				frequencies[word] += 1
			line = text_file.readline()
		top_25 = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)[:25]
		flash(top_25)
	return render_template('index.html')

if __name__ == "__main__":
	app.run()