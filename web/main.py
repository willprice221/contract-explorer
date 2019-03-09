from flask import Flask, abort, redirect, render_template, request
from google.cloud import bigquery
import json
import logging

from loading import load_contract_data
from loading import find_function_in_contract

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
    contract_data = load_contract_data(contract_address)
    return render_template(
        'contract.html',
        contract_address = contract_address,
        functions = contract_data['functions'])

@app.route('/contract/<contract_address>/<function_hash>')
def showFunction(contract_address, function_hash):
    contract_data = load_contract_data(contract_address)
    function = find_function_in_contract(contract_data, function_hash)
    return render_template(
        'function.html',
        contract_address = contract_address,
        function_hash = function_hash,
        function = function)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
