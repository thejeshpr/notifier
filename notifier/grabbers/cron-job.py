import requests

url = "https://api.cron-job.org/"

payload = "{\"email\":\"thejeshpr@gmail.com\",\"password\":\"t6h2e9j2e6s2h\"}"
headers = {
  'Connection': 'keep-alive',
  'Accept': 'application/json, text/plain, */*',
  'X-API-Method': 'Login',
  'X-UI-Language': 'en',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44',
  'Content-Type': 'application/json',
  'Origin': 'https://console.cron-job.org',
  'Sec-Fetch-Site': 'same-site',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'Referer': 'https://console.cron-job.org/login',
  'Accept-Language': 'en-US,en;q=0.9'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))
