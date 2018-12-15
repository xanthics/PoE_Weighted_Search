from urllib import request
import webbrowser
import json

url = "https://www.pathofexile.com/api/trade/search/Delve"
header = {'Content-type': 'application/json',
		  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}

data = input("Enter json query from site: ")

req = request.Request(url, data.encode(), header)

resp = request.urlopen(req)

webbrowser.open_new_tab('https://www.pathofexile.com/trade/search/Betrayal/{}'.format(json.load(resp)['id']))

