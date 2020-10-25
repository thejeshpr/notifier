import requests

url = "https://api.cron-job.org/"

payload = "{\"jobId\":3386798}"
headers = {
  'Connection': 'keep-alive',
  'Accept': 'application/json, text/plain, */*',
  'X-API-Method': 'GetJobHistory',
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MDAxNTQ3ODcsInN1YiI6IjIzOTgwMCIsImdpZCI6IjEiLCJzY3AiOiJzZXNzaW9uIn0.pCA60hUX80knL2ymHihlBPklrbaqyiNaexsxcgZ44FM',
  'X-UI-Language': 'en',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44',
  'Content-Type': 'application/json',
  'Origin': 'https://console.cron-job.org',
  'Sec-Fetch-Site': 'same-site',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'Referer': 'https://console.cron-job.org/jobs/3386798/history',
  'Accept-Language': 'en-US,en;q=0.9'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))
