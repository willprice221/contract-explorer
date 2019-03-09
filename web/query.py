from google.cloud import bigquery
import json
import eth_utils
import pandas as pd
# import numpy as np

client = bigquery.Client()

def get_functions(contract_address):
    adrstr=eth_utils.to_checksum_address(contract_address)
    q = f"""
      SELECT *
      FROM `contract-explorer-233919.ethparis.functions4`
      WHERE addr='{adrstr}'
      """
    query_job = client.query(q)
    results = query_job.result()
    return results.to_dataframe().to_dict('records')
