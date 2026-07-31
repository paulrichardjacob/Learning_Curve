import requests

data_to_be_sent = {
    'number1' : 1,
    'number2' : 2,
    'operation' : 'add'
}

url = 'http://127.0.0.1:5000/calculator'
response = requests.post(data = data_to_be_sent, url=url)

if response.status_code == 200:
    print(response.text)
else:
    print(f'Exiting with an error code {response.status_code}')