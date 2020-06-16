import requests
import timeit
from bs4 import BeautifulSoup
#from conf import *
from Generateurbien import *

url = URLGen()

header = headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

requette = requests.get(url, headers= header)
print(requette)

soup = BeautifulSoup(requette.text, 'lxml')
#print(soup)

size = soup.find("li" ,  {'id' : "NI112O0CL-A110075000" })



print(size)

