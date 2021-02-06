import requests
import base64


def get_json(url):
    response = requests.get(url)
    return response.json()


def encode_file(file):
	with open(file, 'rb') as file:
		encoded_data = base64.b64encode(file.read())
	return encoded_data


def send_json(url, encoded_data, extension, model, vocab):
    params = {'encoded_data': encoded_data, 'ext': extension, 'model': model, 'vocab': vocab}
    response = requests.post(url, data=params)
    return response.json()
