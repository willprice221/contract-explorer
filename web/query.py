from google.cloud import bigquery
import json
import eth_utils
import pandas as pd
# import numpy as np

client = bigquery.Client()

def get_function(function_hash):
    q = f"""
        SELECT *
        FROM `contract-explorer-233919.ethparis.functions11`
        WHERE `hash`='{function_hash}'
        """
    query_job = client.query(q)
    results = query_job.result()
    return results.to_dataframe().to_dict('records')[0]

def get_functions_in_contracts(tree_hash):
    q = f"""
        SELECT *
        FROM `contract-explorer-233919.ethparis.functions11`
        WHERE tree_hash='{tree_hash}'
        LIMIT 100
        """
    query_job = client.query(q)
    results = query_job.result()
    return results.to_dataframe().to_dict('records')

def get_contract_function(contract_address, function_hash):
    adrstr=eth_utils.to_checksum_address(contract_address)
    q = f"""
        SELECT *
        FROM `contract-explorer-233919.ethparis.functions11`
        WHERE addr='{adrstr}' AND `hash`='{function_hash}'
        """
    query_job = client.query(q)
    results = query_job.result()
    return results.to_dataframe().to_dict('records')[0]

def get_functions_w_count(contract_address):
    adrstr=eth_utils.to_checksum_address(contract_address)
    q = f"""
        SELECT * FROM (
          SELECT
            tree_hash,
            name,
            addr,
            `hash`,
            found_count
          FROM  `contract-explorer-233919`.`ethparis`.`functions11`
          JOIN (

          SELECT
            tree_hash,
            count(DISTINCT addr) found_count
          FROM  `contract-explorer-233919`.`ethparis`.`functions11`
          GROUP BY tree_hash

          ) USING (tree_hash)
          WHERE addr='{adrstr}'

        ) JOIN (
          SELECT
            `hash`,
            count(DISTINCT tree_hash) variants_count,
            count(DISTINCT addr) smart_contracts
          FROM  `contract-explorer-233919`.`ethparis`.`functions11`
          GROUP BY `hash`
        ) USING (`hash`)
        ORDER BY found_count DESC
        """
    query_job = client.query(q)
    results = query_job.result()
    return results.to_dataframe().to_dict('records')
