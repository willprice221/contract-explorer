


SELECT
  concat('0x',lower(hex(smart_contract_address_bin))) as smart_contract_address,
  uniq(signature_id) functions,
  count(*) txs
FROM production.calls_sc
GROUP BY smart_contract_address_bin
HAVING functions<50
ORDER BY functions*txs DESC
LIMIT 50000
INTO OUTFILE 'top_contracts.csv' FORMAT CSV



SELECT
  concat('0x',lower(hex(smart_contract_address_bin))) as smart_contract_address,
