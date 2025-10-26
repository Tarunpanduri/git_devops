from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Updated template

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/todo')
def todo():
    return render_template('todo.html')

@app.route('/success')
def success():
    return "<h2>Data submitted successfully!</h2>"

if __name__ == '__main__':
    app.run(port=5001, debug=True)
