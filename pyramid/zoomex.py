import requests

url = "https://zoom.us/oauth/token?grant_type=authorization_code&code={code}&redirect_uri={yourOAuthAppsRedirectUri}"

payload = {}
headers = {
  'Authorization': 'Basic NnJFU2NHdU5UbGFOOThNM2NoVXNoQTpwMXhqS1dvNXhpVEt0aExpNDdEcVFMSzUzeE0zN0tQcw=='
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))