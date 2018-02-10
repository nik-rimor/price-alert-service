__author__ = "nik"

import requests
from bs4 import BeautifulSoup
import re

request = requests.get("https://www.smile-pharmacy.gr/vendors/korres/korres-echinacea-amp-vitamin-c-20-%CE%B1%CE%BD%CE%B1%CE%B2%CF%81%CE%B1%CE%B6%CE%BF%CF%85%CF%83%CE%B5%CF%83-%CF%84%CE%B1%CE%BC%CF%80%CE%BB%CE%B5%CF%84%CE%B5%CF%83-1-1.htm")
content = request.content
soup = BeautifulSoup(content, "html.parser")
element = soup.find("span", {"class": "col-xs-12 col-sm-6 col-md-12 homeprice"})

#list1=soup.find_all("a",{"class":"product-link js-product-link content-placeholder"})
#for item in list1:
#    print(item.text)
string1=element.text.strip().replace("\n","").replace("\r","").replace(" ","")
pattern = re.compile("(\d+.\d+)")
match = pattern.search(string1)
price = match.group()
print(price)






