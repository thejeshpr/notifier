
import urllib3

http = urllib3.PoolManager()

url = 'https://9gag.com/v1/group-posts/group/car/type/trending'
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
response = http.request('GET', url, headers=headers)
# print(dir(response))

print(response.data.decode("utf-8"))
