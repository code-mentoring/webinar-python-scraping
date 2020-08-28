import urllib.request
import json
from datetime import date
from bs4 import BeautifulSoup


opener = urllib.request.FancyURLopener({})
url = "https://coinmarketcap.com/"
f = opener.open(url)
content = f.read()
soup = BeautifulSoup(content, 'html.parser')

table = soup.select('div.cmc-table tbody', class_="cmc-table")[0]
trs = table.find_all('tr')

coins = {}

for tr in trs: # Loop over all the TRs in the tbody
  tdName = tr.select('tr td:nth-child(2)')
  if not tdName: continue # Probably an ad
  name = tdName[0].get_text()
  tdPrice = tr.select('tr td:nth-child(4)')
  price = float(
    tdPrice[0].get_text()
      .replace('$', '')
      .replace(',', '')
  )
  coins[name] = price


with open('coins.json') as read:
  data = json.load(read)
  data[str(date.today())] = coins

  with open('coins.json', 'w') as outfile:
    json.dump(data, outfile)
