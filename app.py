from flask import Flask, render_template


# defaults
app = Flask(__name__)




#routes
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')