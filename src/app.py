from flask import Flask

app = Flask(__name__)

@app.route('/')
def pga_details():
    return 'Total Memebers is 30'

@app.route('/absent')
def absentees():
    return '5 Member are absent'

@app.route('/present')
def present():
    return '25 Member are present'

app.run(debug = True)