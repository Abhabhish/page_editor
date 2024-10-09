import requests

get_response = requests.get("http://127.0.0.1:8000/api/page_content/maps/rajasthan/index.html/")

print(get_response.json())


