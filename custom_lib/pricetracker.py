import requests
from bs4 import BeautifulSoup
from pprint import pprint 
import base64
import time
import json

import argparse



def get_price(product_url: str):	
	auth = base64.b64encode( ("ajax:true-" + str(int(time.time()))).encode("utf-8") )
	auth = "Basic " + str(auth, "utf-8")
	print(auth)


	client = requests.Session()
	res = client.get("https://pricehistory.in/")
	print(client.cookies, "\n\n")

	time.sleep(1)

	headers = {
	  'authority': 'pricehistory.in',
	  'accept': 'application/json, text/javascript, */*; q=0.01',
	  'x-requested-with': 'XMLHttpRequest',  
	  'Authorization': auth,
	  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
	  'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
	  'origin': 'https://pricehistory.in',
	  'sec-fetch-site': 'same-origin',
	  'sec-fetch-mode': 'cors',
	  'sec-fetch-dest': 'empty',
	  'referer': 'https://pricehistory.in/',
	  'accept-language': 'en-US,en;q=0.9',
	  'cookie': f'__cfduid={res.cookies.get("__cfduid")}; _ga=GA1.2.1037178724.1599729668; _gid=GA1.2.2074719493.1601003656; XSRF-TOKEN={res.cookies.get("XSRF-TOKEN")}; _gat_gtag_UA_50001635_52=1; price_history_session={res.cookies.get("price_history_session")}'
	}

	pprint(headers)
	print("\n\n")

	soup = BeautifulSoup(res.content, 'html.parser')
	tkn = soup.find("input", {"name":"_token"}).get("value")

	print("Token:", tkn)

	payload = f"product_url=https%3A%2F%2Fwww.myntra.com%2Ftshirts%2Fhrx-by-hrithik-roshan%2Fhrx-by-hrithik-roshan-men-navy-advanced-rapid-dry-round-neck-t-shirt%2F2314400%2Fbuy&_token={tkn}"

	data = {
		# "product_url": "https://www.myntra.com/sunglasses/hrx-by-hrithik-roshan/hrx-by-hrithik-roshan-men-oval-sunglasses-mfb-pn-cy-56018/2311920/buy",
		"product_url": product_url,
		"_token": tkn
	}

	print("Payload:", data, "\n\n")


	response = client.post("https://pricehistory.in/api/productHistory", headers=headers, data=data)

	print(response)
	pprint(response.json())


	print(response.cookies.get_dict())
	return response.json()

	# with open("sample-res.json", "w") as fd:
	# 	fd.write(str(response.json()))

	# response_data = response.json()

	# data = json.loads(response_data['data'])

	# for row in data:
	# 	ts = int(str(row[0])[:-3])
	# 	#print(ts)
	# 	price = row[1]
	# 	print(time.ctime(ts), '--->', price)

	# print('high_price:', response_data['high_price'])
	# print('low_price:', response_data['low_price'])
	# print('curr_price:', response_data['curr_price'])


# def main():
# 	parser = argparse.ArgumentParser()
# 	parser.add_argument("product_url")
# 	args = parser.parse_args()
# 	get_price(args.product_url)

# if __name__ == '__main__':
# 	main()
