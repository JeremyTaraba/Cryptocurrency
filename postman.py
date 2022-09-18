import requests

url = "https://api.twitter.com/2/tweets/search/recent?query=cryptocurrency&max_results=100"

payload={}
headers = {
  'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAJtbgwEAAAAAEAieskSy%2FW9LFVVj%2BuUeW39%2FRMU%3DyavmJg7HfhZQYKCViV23zQnnjtn2C1VKUtl7daHFfBHGvzqRcC',
  'Cookie': 'guest_id=v1%3A166319300522636822'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)