from urllib import request
import webbrowser
import json

url = "https://www.pathofexile.com/api/trade/exchange/Delirium"
header = {'Content-type': 'application/json',
		  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}

data = '''{"exchange":{"want":["chaos"],"have":["exa"],"status":"online"}}'''  # input("Enter json query from site: ")

req = request.Request(url, data.encode(), header)

resp = json.load(request.urlopen(req))
print(resp)
#webbrowser.open_new_tab('https://www.pathofexile.com/trade/exchange/Delirium/{}'.format(resp['id']))

