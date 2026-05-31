import requests
try:
    resp = requests.post("http://127.0.0.1:5000/ask", json={"query": "hai"})
    print(resp.status_code)
    print(resp.text)
except Exception as e:
    print("Error:", e)
