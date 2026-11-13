from flask import Flask, request

app = Flask(__name__)

OPERATIONS = {
    'add': ('+', lambda a, b: a + b),
    'subtract': ('-', lambda a, b: a - b),
    'multiply': ('*', lambda a, b: a * b),
    'divide': ('/', lambda a, b: a / b),
}


@app.route('/calculator', methods=['POST'])
def calculator():
    try:
        num1 = float(request.form['number1'])
        num2 = float(request.form['number2'])
    except (KeyError, ValueError):
        return "number1 and number2 are required and must be numbers", 400

    operation = request.form.get('operation', '')
    if operation not in OPERATIONS:
        return f"Unsupported operation '{operation}'. Use one of: {', '.join(OPERATIONS)}", 400

    if operation == 'divide' and num2 == 0:
        return "Cannot divide by zero", 400

    symbol, func = OPERATIONS[operation]
    return f"{operation.capitalize()} of two numbers: {num1} {symbol} {num2} = {func(num1, num2)}"


if __name__ == '__main__':
    app.run(debug=True)
