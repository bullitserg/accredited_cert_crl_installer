get_accredited_info_query = '''SELECT
  aci.subjKeyId,
  aci.serial,
  aci.sha1Hash,
  aci.crlUrl,
  aci.location
FROM accredited_cert_info aci
WHERE aci.fileVersion = (SELECT
    MAX(aci.fileVersion)
  FROM accredited_cert_info
  WHERE aci.active = 1
  AND aci.archive = 0)
AND aci.active = 1
AND aci.archive = 0;'''
