import bs4 
import requests

response = requests.get('https://www.msn.com/es-mx/')
res = response.content
soup = BeautifulSoup(res)

h1 = soup.find("h1", {"class": "page_title"})
print(h1.string)

#bs.html.body.div