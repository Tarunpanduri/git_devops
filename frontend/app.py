from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('admin.html')

@app.route('/success')
def success():
    return "<h2>Data submitted successfully!</h2>"

if __name__ == '__main__':
    app.run(port=5001, debug=True)
