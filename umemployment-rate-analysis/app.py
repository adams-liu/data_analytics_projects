import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.newegg.ca/p/pl?d=graphics+cards'
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

#grabs each product
containers = page_soup.findAll("div",{"class": "item-cell"})

brand = containers[0].div.div.a.img['title']
title = containers[0].find("a",{"class":"item-title"}).text

# Write HTML String to file.html
with open("file.html", "w") as file:
    file.write(str(container))
print(container)

