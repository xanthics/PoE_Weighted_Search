from urllib import request
import webbrowser
import json

url = "https://www.pathofexile.com/api/trade/search/Delve"
header = {'Content-type': 'application/json'}

data = input("Enter json query from site: ")

req = request.Request(url, data.encode(), header)

resp = request.urlopen(req)

webbrowser.open_new_tab('https://www.pathofexile.com/trade/search/Delve/{}'.format(json.load(resp)['id']))

