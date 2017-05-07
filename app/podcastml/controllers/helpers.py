# Methods to compose HTTP response JSON 
from flask import jsonify

from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

def http_json(result, bool):
	result.update({ "success": bool })
	return jsonify(result)


def http_resource(result, name, bool=True):
	resp = { "data": { name : result }}
	return http_json(resp, bool)


def http_errors(result): 
	errors = { "data" : { "errors" : result.errors["_schema"] }}
	return http_json(errors, False)

def processText(s):
	return BeautifulSoup(s,"html.parser").text

def set_builder(lst):
	output = []
	for l in lst:
		output+=list(set(l))
	return list(set(output))