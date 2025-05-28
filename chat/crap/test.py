import requests


# Base URL of the API
API_BASE_URL = "http://localhost:8000"

# Endpoint path
GET_CHAT_USERS_ENDPOINT = "/api/channel/get/list/brief"

# Access token (zwykle uzyskiwane podczas logowania)
REFRESH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0ODUzMzQ0OCwiaWF0IjoxNzQ4NDQ3MDQ4LCJqdGkiOiI1NTYxNzA2NTg0MDA0NTc2YmY0ZjM2OGQwMjIxOTA0YiIsInVzZXJfaWQiOjEsInVzZXJuYW1lIjoiYWRtaW4iLCJmaXJzdF9uYW1lIjoiIiwibGFzdF9uYW1lIjoiIiwiYXV0aG9yaXR5IjozfQ.H_UzDsFuyfICv_tPtyg2dlYViqaCAt1hl5ErlNCMA6Q"
REFRESH_TOKEN_Janek = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0ODU0NDE1NCwiaWF0IjoxNzQ4NDU3NzU0LCJqdGkiOiJhMGU5NzZlYjA0ZTI0NTJhYTlmOWQ5ZmVjZWVjOTRmZSIsInVzZXJfaWQiOjMsInVzZXJuYW1lIjoiamFuZWsiLCJmaXJzdF9uYW1lIjoiSmFuIiwibGFzdF9uYW1lIjoiQmFraW5vd3NraSIsImF1dGhvcml0eSI6MX0.aEgZcCXPmf02OzHyASMP5ZRqshs-bDf8EWJ7EEPUfUA"
REFRESH_TOKEN_Nowy =  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0ODU0NDM2MiwiaWF0IjoxNzQ4NDU3OTYyLCJqdGkiOiI3ZDRmZjcxMmI4NmE0YmMyYTYxZTRlNjE5NDEwNzc2ZCIsInVzZXJfaWQiOjQsInVzZXJuYW1lIjoiTm93eSIsImZpcnN0X25hbWUiOiJOb3d5IiwibGFzdF9uYW1lIjoiWmFyZWplc3Ryb3dhbnkiLCJhdXRob3JpdHkiOjF9.qTsAOsm66lonO6sTQHWUcAWZfS2AU5AEhH1mf5Kyyo8"

def get_new_access_token(refresh_token):
    Endpoint = "http://localhost:8000/api/user/refresh/"
    r = requests.post(Endpoint, data={"refresh": refresh_token})
    return r.json()["access"]

ACCESS_TOKEN = get_new_access_token(REFRESH_TOKEN_Nowy)

# Full URL
url = f"{API_BASE_URL}{GET_CHAT_USERS_ENDPOINT}"

# Headers, z tokenem uwierzytelnienia
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Sending GET request
response = requests.get(url, headers=headers)

# Verifying the response
if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.status_code, response.text)

