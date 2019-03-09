from flask import Flask, abort, redirect, render_template, request
import json
import logging

from query import *
from source_code import contract_function_code
from predict import predict_model

app = Flask('content-explorer')

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
    function = get_function(contract_address, function_hash)
    functions_exact = get_functions_in_contracts(function['tree_hash'])
    function_sources = contract_function_code(contract_address, function_hash)
    return render_template(
        'function.html',
        contract_address = contract_address,
        function_hash = function_hash,
        function = function,
        functions_exact = functions_exact,
        function_sources = function_sources)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
