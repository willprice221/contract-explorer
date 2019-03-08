from google.cloud import bigquery
from google.oauth2 import service_account
import json
import eth_utils

credentials = service_account.Credentials.from_service_account_file('/Users/studnev/daoready/spy/log/ethparis/api-project-253388791536-3a7207b7f8e1.json')
project_id = 'api-project-253388791536'
client = bigquery.Client(credentials=credentials,project=project_id)

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
            trees.append({'addr': d['addr'], 'hash': f['hash'], 'tree': f['trace']})
    return trees

x = contract_trees(['0x2ad180cbaffbc97237f572148fc1b283b68d8861','0x39d77a9dbea6aec36adbb84de0be18aac1aa21b0'])

