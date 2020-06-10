import requests
import bs4
import random
import webbrowser


# Base URL = https://www.zalando.fr/nike-sportswear-air-force-1-07-an20-baskets-basses-whiteblack-ni112o0cl-a11.html
# Base URL = https://www.zalando.fr/nike-sportswear-air-max-2090-baskets-basses-whiteblackpure-platinumbright-crimsonwolf-greyblue-hero-ni112o0cd-a11.html


def URLGen(model, ref, coul, type_):
	
	
	
	URL = 'https://www.zalando.fr/' + str(type_)+ "-" + str(model) + "-" + str(coul) + "-" + str(ref) + ".html"
	return URL


#type_ = input ("Entrer le type de produit :")
type_=str('Nike Sportswear')
type_= type_.lower()
type_= type_.replace(" ", "-")

#Model = input('Model #: ')
Model =str('AIR FORCE 1 ’07 AN20  - Baskets basses')
Model = Model.lower()
Model= Model.replace("’","")
Model= Model.replace("  "," ")
Model= Model.replace(" - ","-")
Model= Model.replace(" ","-")

#reference = input('Reference : ')
reference =str("NI112O0CL-A11") 
reference= reference.lower()

#couleur= input( "couleur :")
couleur=str("white/black")
couleur= couleur.replace("/", "")



URL = URLGen(Model, reference, couleur, type_)


print(URL)

def Verifie_stock(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	RawHTML = requests.get(url, headers=headers)
	Page = bs4.BeautifulSoup(RawHTML.text, "lxml")
	print(Page.title.string)
	listedestailles = Page.select('.UyCaZm._2TPICz.mAhwAe.FIoNYa')
	Sizes = str(listedestailles)
	print(Sizes)



	'''Sizes = str(listedestailles[0].getText()).replace('\t', '')
	Sizes = Sizes.replace('\n\n', ' ')
	
	Sizes = Sizes.split()
	Sizes.remove('Select')
	Sizes.remove('size')
	for size in Sizes:
		print(' Tailles: ' + str(size) + ' Disponible')'''


	
url = URLGen(Model, reference, couleur, type_)
Verifie_stock(url)