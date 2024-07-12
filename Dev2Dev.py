import requests
import json

#Get the Bearer Token for Authentication 
def get_token(clientId,clientSecret):
    url = "https://api.us1.plainid.io/api/1.0/api-key/token"
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": clientId,
        "client_secret": clientSecret
    }
    response = requests.post(url, headers=headers, data=data, verify=False)

    data = response.json()
    extract_data = data['access_token']
    BEARER_TOKEN = str(extract_data)

    return BEARER_TOKEN


BEARER_TOKEN = get_token("P3VPGSJZWBW9TTBRBKZL","MDyFt5eFZLaHslYt5MTUBMcOXyEjg2UA")

print(BEARER_TOKEN)



#Get the logs from plainID
def get_audit_admin_logs(envId, timestamp, resource_type,limit,offset):
    url = f"https://api.us1.plainid.io/api/1.0/audit-admin/{envId}"

    params = {
        "filter[timestamp][gt]": timestamp,
        "filter[resourceType][eq]": resource_type,
        "limit": limit,
        "offset": offset
    }

    headers = {
        'Authorization': 'Bearer ' + BEARER_TOKEN,
        'accept': 'application/json'
    }

    response = requests.get(url, headers=headers, params=params)
    plainid_data = response.json()
    plainid_data_json = json.dumps(plainid_data, indent=4)
    print(plainid_data_json)
    return plainid_data_json



envId = "13397a05-a1d1-48f8-8367-42cc60311be1"
#envId = "5e648a8c-11c6-4a3f-9342-184300a71930"

timestamp = "1717207543000"
resource_type = "ROLE"
limit = 50
offset = 0

plainid_data_json = get_audit_admin_logs(envId, timestamp, resource_type,limit,offset)



#Send audit admin logs from plainID to Splunk

def send_to_splunk(hec_token, data, url):
    headers = {
        'Authorization': 'Splunk ' + hec_token,
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "sourcetype": "plainid:audit",
        "event": plainid_data_json
    })
    response = requests.post(url, headers=headers, data=payload, verify=False)
    print(response.text)
    

splunk_hec_url = "https://sra-lb-dmz-nprd.cisco.com/services/collector"

send_to_splunk(HEC_TOKEN, plainid_data_json, splunk_hec_url)
