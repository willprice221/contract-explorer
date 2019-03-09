


SELECT
  DISTINCT smart_contract_address
FROM (
  SELECT
    concat('0x',lower(hex(smart_contract_address_bin))) as smart_contract_address
  FROM production.calls_sc
  GROUP BY smart_contract_address_bin
  HAVING uniq(signature_id)<50
  ORDER BY uniq(signature_id)*count(*) DESC
  LIMIT 100000

  UNION ALL

  SELECT
    dictGetString('currency', 'address', toUInt64(currency_id)) AS smart_contract_address
  FROM  production.transfers_currency
  WHERE currency_id!=1
  GROUP BY currency_id
  ORDER BY count(*) DESC
  LIMIT 50000
) INTO OUTFILE 'top_tokens_sc2.csv' FORMAT CSV

