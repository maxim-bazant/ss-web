from auth_setup import AUTH0_CLIENT_ID, AUTH0_DOMAIN, AUTH0_CLIENT_SECRET
import json

import http.client

def get_token():
    conn = http.client.HTTPSConnection("storage-solution.eu.auth0.com")

    payload = "{\"client_id\":\"K6Bs1ktSLDDbQPwushM6h4VUvl1RGRFU\",\"client_secret\":\"fmJAHYlASbCjQnyhxzxKnNV-iWnTdc60DFlPAuiyGw4qJZB1LqjGjTCOkr-6EyNd\",\"audience\":\"https://storage-solution.eu.auth0.com/api/v2/\",\"grant_type\":\"client_credentials\"}"
    headers = { 'content-type': "application/json" }

    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    decoded_data = json.loads(data.decode("utf-8"))
    
    return decoded_data["access_token"]



def has_admin_role(user_id):
    conn = http.client.HTTPSConnection("storage-solution.eu.auth0.com")

    headers = { 'authorization': f"Bearer {get_token()}" }

    conn.request("GET", f"/api/v2/users/{user_id}/roles", headers=headers)

    res = conn.getresponse()
    data = res.read()
    decoded_data = json.loads(data.decode("utf-8"))

    for role in decoded_data:
        if role["name"] == "admin":
            return True
    
    return False