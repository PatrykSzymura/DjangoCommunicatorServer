# code for triggering notifications
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_user_notification(user_id, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {
            "type": "send_notification",
            "message": message,
        },
    )

import requests

# Base URL of the API
API_BASE_URL = "http://localhost:8000"

# Endpoint path
GET_CHAT_USERS_ENDPOINT = "/api/channel/members/get/"

# Access token (zwykle uzyskiwane podczas logowania)
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3Nzg2MTcwLCJpYXQiOjE3NDc3ODU4NzAsImp0aSI6IjIwMjA3NmI3M2E1ZDQwODE5MTk4YjhkNGE5NjM4NWFlIiwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJhZG1pbiIsImZpcnN0X25hbWUiOiIiLCJsYXN0X25hbWUiOiIiLCJhdXRob3JpdHkiOjN9.RD-9-BBGb4E34lWaq48tRZx4MQynhAsBgpfNl9LkgN0"

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

