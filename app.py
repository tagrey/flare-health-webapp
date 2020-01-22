from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/upload_document")
def upload_document():
	return

if __name__ == "__main__":
    app.run()