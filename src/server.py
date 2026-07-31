from flask import Flask, request

app = Flask(__name__)

@app.route('/calculator', methods = ['POST'])
def calculator():
    num1 = float(request.form['number1'])
    num2 = float(request.form['number2'])
    operation = request.form['operation']
    
    if operation == 'add':
        return f"Addtion of two number {num1} + {num2} = {num1+num2}"
    

app.run(debug = True)
    