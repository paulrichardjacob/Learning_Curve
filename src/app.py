from flask import Flask

app = Flask(__name__)

@app.route('/')
def pga_details():
    return 'Total Members is 30'

@app.route('/absent')
def absentees():
    return '5 Members are absent'

@app.route('/present')
def present():
    return '25 Members are present'

if __name__ == '__main__':
    app.run(debug=True)
