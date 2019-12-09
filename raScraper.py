import requests
import pandas as pd
from toolz.curried import pipe, map, curry
from functional import seq
import time

from bs4 import BeautifulSoup
festival_dict = {}
base_url = 'http://www.residentadvisor.net/features.aspx?series=festivals'
#get all top 10 festival urls
page = requests.get("http://www.residentadvisor.net/features.aspx?series=festivals")
soup = BeautifulSoup(page.content, 'html.parser')
top_10_festival_urls  = seq(soup.findAll("a", title=lambda title: title and "2019" in title ))\
  .map(lambda item: item.attrs['href'])
#top_10_festival_urls = list(map(lambda item: item.attrs['href'], top_10_festival_urls))
for url in top_10_festival_urls :
  page = requests.get("http://www.residentadvisor.net/" + url )
  soup = BeautifulSoup(page.content, 'html.parser')
  festivals = soup.findAll("a", href=lambda href: href and "events/" in href )
  for festival in festivals: 
      festival_item  = { "name": festival.contents[0]}
      page = requests.get("http://www.residentadvisor.net/" +  festival.attrs['href'] )
      soup = BeautifulSoup(page.content, 'html.parser')
      djs = seq(soup.findAll("a", href=lambda href: href and "/dj/" in href ))\
        .map(lambda item : item.contents[0]) 
      festival_item["djs"] = djs
      festival_dict[festival_item["name"]] = festival_item
      time.sleep(10)

df = pd.DataFrame(festival_dict)
df.to_csv("./festivals.csv")

