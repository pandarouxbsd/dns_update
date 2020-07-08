#!/usr/bin/env python3

import requests, json
import os

domain = os.environ.get("DOMAIN")
gandi_api_url = "api.gandi.net/v5/livedns/"
ipinfo_url = "ipinfo.io"

GANDI_API_KEY = os.environ.get("GANDI_API_KEY")
if GANDI_API_KEY == None:
	raise EnvironmentError("Missing key GANDI_API_KEY")

url_get_domain = f"https://{gandi_api_url}/domains/{domain}/records"
headers = {}
headers["Content-Type"] = "application/json"
headers["authorization"] = f"Apikey {GANDI_API_KEY}"

response_getdomain = requests.request("GET", url_get_domain, headers=headers)
getdomain_json = json.loads(json.dumps(response_getdomain.json()))
for elem in getdomain_json:
	if elem["rrset_type"] == "A" and elem["rrset_name"] == "@":
		gandi_ipv4 = elem["rrset_values"][0]
		break

ipinfo_response = requests.request("GET", f"http://{ipinfo_url}/json")
ipinfo_json = json.loads(json.dumps(ipinfo_response.json()))
current_ipv4 = str(ipinfo_json["ip"])

url_update_domain = f"https://{gandi_api_url}/domains/{domain}/records/@/A"
updated_record = {}
updated_record["rrset_type"] = "A"
updated_record["rrset_values"] = [current_ipv4]
updated_record_json = json.dumps(updated_record)

if (current_ipv4 != gandi_ipv4):
	res = requests.put(url_update_domain, headers=headers, data=updated_record_json)
	if (res.status_code != 200):
		raise ValueError(f"Status code incorrect when calling {url_update_domain} ({res.status_code}): {res.text}")
	print("IP changed")
else:
	print("IP checked, no changes.")
