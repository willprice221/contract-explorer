from flask import Flask, abort, redirect, render_template, request
import json
import logging
from operator import itemgetter

from functions import *
from query import *
from source_code import contract_function_code
from predict import predict_model

app = Flask('content-explorer', static_folder='static', static_url_path='')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contract', methods=['POST'])
def submitContract():
    address = request.form.get('address')
    return redirect('/contract/%s' % address)

@app.route('/contract/<contract_address>')
def showContract(contract_address):
    contract_functions = get_functions_w_count(contract_address)
    return render_template(
        'contract.html',
        contract_address = contract_address,
        functions = contract_functions)

@app.route('/contract/<contract_address>/<function_hash>')
def showFunction(contract_address, function_hash):
    function = get_contract_function(contract_address, function_hash)
    functions_exact = get_functions_in_contracts(function['tree_hash'])
    function_sources = contract_function_code(contract_address, function_hash)

    top_probs, top_fhashes = predict_model(function['tree'])
    top_funcs = [get_function(h) for h in top_fhashes]
    functions_prediction = sorted(zip(top_probs, top_funcs), key=itemgetter(0), reverse=True)

    return render_template(
        'function.html',
        contract_address = contract_address,
        function_hash = function_hash,
        function = function,
        functions_exact = functions_exact,
        functions_prediction = functions_prediction,
        function_sources = function_sources)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
