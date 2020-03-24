from bs4 import BeautifulSoup
import requests


response = requests.get("https://www.sslproxies.org")
soup = BeautifulSoup(response.content, "html.parser")

rows = soup.find_all("tr")[1:]

lst = []
i = 0
while True:
	try:
		if 'Brazil' in str(rows[i]):
			split = str(rows[i]).split("<td>")
			lst.append(split[1][:-5] + ":" + split[2][:-5])
		i = i+1
	except:
		break

jsonstr = "{"

for l in lst:
	jsonstr = jsonstr + f"\"https\": \"https://{l}\", "
jsonstr = jsonstr[:-2] + "}"

print(jsonstr)

with(open("proxies.txt", "w")) as f:
	f.write(jsonstr)
