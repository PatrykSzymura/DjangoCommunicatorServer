import requests


# Base URL of the API
API_BASE_URL = "http://localhost:8000"

# Endpoint path
GET_CHAT_USERS_ENDPOINT = "/api/user/get/current/1"

# Access token (zwykle uzyskiwane podczas logowania)
REFRESH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NzkwNzc4NCwiaWF0IjoxNzQ3ODIxMzg0LCJqdGkiOiJiYzg2YmJiYWQxZDc0NmQ2YTY0YTAzYmM5YTI0MTc4MCIsInVzZXJfaWQiOjEsInVzZXJuYW1lIjoiYWRtaW4iLCJmaXJzdF9uYW1lIjoiIiwibGFzdF9uYW1lIjoiIiwiYXV0aG9yaXR5IjozfQ.x_M2nlrdyqp6Buah4HtEoCr4yneSD5j-bYMsIvi1AqE"
REFRESH_TOKEN_Janek = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NzkwOTM3NCwiaWF0IjoxNzQ3ODIyOTc0LCJqdGkiOiJlODAzZmMwNmNmYzg0MDFmOGI4N2I5MWRjMDdmZjhhYyIsInVzZXJfaWQiOjMsInVzZXJuYW1lIjoiamFuZWsiLCJmaXJzdF9uYW1lIjoiIiwibGFzdF9uYW1lIjoiIiwiYXV0aG9yaXR5IjoxfQ.mVNVbhzIPWKJrmpGvwQogS-RhtTjl87pTWPoH0nkXAk"

def get_new_access_token(refresh_token):
    Endpoint = "http://localhost:8000/api/user/refresh/"
    r = requests.post(Endpoint, data={"refresh": refresh_token})
    return r.json()["access"]

ACCESS_TOKEN = get_new_access_token(REFRESH_TOKEN_Janek)

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

