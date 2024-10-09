import requests

endpoint = "http://localhost:8000/api/page_content/"

get_response = requests.post(endpoint,data={"slug": "maps/rajasthan/index.html"})

print(get_response.json())

