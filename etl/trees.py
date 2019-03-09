from google.cloud import bigquery
from google.oauth2 import service_account
import json
import eth_utils
import pandas as pd
import numpy as np
import hashlib


credentials = service_account.Credentials.from_service_account_file('/Users/studnev/daoready/spy/log/ethparis/contract-explorer-233919-30765f8edb40.json')
project_id = 'contract-explorer-233919'
client = bigquery.Client(credentials=credentials,project=project_id)


### --- query veem --

def contract_trees(addresses):
    adrstr = ', '.join(map(lambda x: '\''+eth_utils.to_checksum_address(x)+'\'', addresses))
    size = len(addresses)
    q = f"""
      SELECT contract
      FROM  `showme-1389.eveem`.`contracts`
      WHERE ver='v4' AND addr IN ({adrstr}) LIMIT {size}
      """
    query_job = client.query(q)
    results = query_job.result()
    trees = []
    for row in results:
        d = json.loads(row[0])
        for f in d['functions']:
            tree_str = json.dumps(f['trace'])
            tree_hash = hashlib.sha1(tree_str.encode()).hexdigest()
            trees.append({'addr': d['addr'], 'hash': f['hash'], 'tree': tree_str, 'name': f['name'], 'signature': f['abi_name'], 'tree_hash': tree_hash})
    return trees

x = contract_trees(['0x2ad180cbaffbc97237f572148fc1b283b68d8861','0x39d77a9dbea6aec36adbb84de0be18aac1aa21b0'])


### ---- parse and load from CSV list

def load_functions_in_bigquery(addresses,table_name='test'):
    ref = bigquery.table.TableReference.from_string('contract-explorer-233919.ethparis.'+table_name)
    trees=contract_trees(addresses)
    data = pd.DataFrame(trees,index=None)
    load_job = client.load_table_from_dataframe(data,ref)
    load_job.result()


def load_list_from_csv_to_bigquery(csv_file,table_name='test', in_batch=100):
    contracts = pd.io.parsers.read_csv('/Users/studnev/daoready/contract-explorer/etl/top_contracts.csv',header=None)
    iteration = 0
    batches = len(contracts)/in_batch
    for addr_arry in np.array_split(contracts[0], batches):
        iteration += 1
        print(f'Running iteration {iteration} out of {batches}...')
        load_functions_in_bigquery(list(addr_arry),table_name)
    return 'Done'

load_list_from_csv_to_bigquery('/Users/studnev/daoready/contract-explorer/etl/top_contracts.csv','functions3',1000)



### --- read the result


def get_functions(address):
    adrstr=eth_utils.to_checksum_address(address)
    q = f"""
      SELECT *
      FROM  `api-project-253388791536.ethparis_trees`.`functions`
      WHERE addr='{adrstr}'
      """
    query_job = client.query(q)
    results = query_job.result()
    return results.to_dataframe()

get_functions('0x39d77A9DBEA6AEc36adBb84DE0be18AAC1aA21b0')
