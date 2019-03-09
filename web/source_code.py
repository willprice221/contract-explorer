from google.cloud import bigquery
import eth_utils
import json
import pandas as pd
import re

client = bigquery.Client()

colors = {
    '\033[95m': '235, 97, 247', #COLOR_HEADER =
    '\033[91m': '236, 89, 58', # fail
    '\033[38;5;8m': '111, 110, 111', # gray
    '\033[32m': '107, 194, 76', # green
    '\033[93m': '239, 236, 84', # warning
    '\033[92m': '119, 232, 81', # okgreen
    '\033[94m': '184, 90, 190' # "blue", yeah, right
}

def convert(text):

    for asci, html in colors.items():
        text = text.replace(asci, '<span style="color:rgb(' + html + ')">')

    text = text.replace('\033[1m','<span style="font-weight:bold">')

    text = re.sub(r'»#(.*)\n', '<span style="color:rgb(111, 110, 111)">#\\1</span>\n', text)

    text = text.replace('»', '&raquo;')

    text = text.replace('\033[0m', '</span>')

    return text

def contract_function_code(contract_address, function_hash):
    adrstr = eth_utils.to_checksum_address(contract_address)
    q = f"""
      SELECT contract
      FROM  `showme-1389.eveem`.`contracts`
      WHERE ver='v4' AND addr='{adrstr}' LIMIT 1
      """
    query_job = client.query(q)
    results = query_job.result().to_dataframe()
    functions = json.loads(results['contract'][0])['functions']
    code = next(f for f in functions if f["hash"] == function_hash)['print']
    return convert(code)

# contract_function_code('0x2ad180cbaffbc97237f572148fc1b283b68d8861','0x095ea7b3')
