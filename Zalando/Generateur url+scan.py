import requests
import bs4
import random
import webbrowser


# Base URL = https://www.zalando.fr/nike-sportswear-air-force-1-07-an20-baskets-basses-whiteblack-ni112o0cl-a11.html
# Base URL = https://www.zalando.fr/nike-sportswear-air-max-2090-baskets-basses-whiteblackpure-platinumbright-crimsonwolf-greyblue-hero-ni112o0cd-a11.html


def URLGen(model, ref, coul, type_):
	
	
	
	URL1 = 'https://www.zalando.fr/' + str(type_)+ "-" + str(model) + "-" + str(coul) + "-" + str(ref) + ".html"
	URL2='https://www.zalando.fr/' + str(type_)+ "-" + str(model) + "-" + str(ref) + ".html"

	URLs= [URL1, URL2]
	return URLs


#type_ = input ("Entrer le type de produit :")
type_=str('adidas Originals')
type_= type_.lower()
type_= type_.replace(" ", "-")

#Model = input('Model #:')
Model =str('COAST STAR - Baskets basses')
Model = Model.lower()
Model= Model.replace("’","")
Model= Model.replace("  "," ")
Model= Model.replace(" - ","-")
Model= Model.replace(" ","-")

#couleur= input( "couleur :")
couleur=str("footware white/collegiate navy")
couleur= couleur.replace("/", "")
couleur= couleur.replace(" ", "-")

#reference = input('Reference :')
reference =str("AD115O0K7-A11") 
reference= reference.lower()





URL = URLGen(Model, reference, couleur, type_)

liste_tailles=[38,39,40,41,42,43,44,45,46,47,48,49,50]

print(URL[0], "\n" , URL[1])

def Verifie_stock(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	RawHTML = requests.get(url, headers=headers)
	print(RawHTML.status_code)
	Page = soup.BeautifulSoup(RawHTML.text, "lxml")
	print(Page.title.string)

	button =soup.find_all("button")
	#listedestailles = Page.select('button')
	Sizes = str(listedestailles)
	#print(Sizes)

	for button in liste_tailles:
		if "38" or "39" or "40" or "41" or "42" or "43" or "44" or "45" or "46" in button.text:
			print(button)


	'''Sizes = str(listedestailles[0].getText()).replace('\t', '')
	Sizes = Sizes.replace('\n\n', ' ')
	
	Sizes = Sizes.split()
	Sizes.remove('Select')
	Sizes.remove('size')
	for size in Sizes:
		print(' Tailles: ' + str(size) + ' Disponible')'''


URL = URLGen(Model, reference, couleur, type_)
Verifie_stock(URL[0])



'''def SneakerBot(model, size=None):
	while True:
		try:
			url = 'http://www.adidas.com/us/{}.html?'.format(model)
			Sizes = CheckStock(url)
			if size != None:
				#If you didn't input size
				if str(size) in Sizes:
					DoSomething()
			else:
				for a in Sizes:
					DoSomething()
		except:
			pass

threads = [threading.Thread(name='ThreadNumber{}'.format(n), target=SneakerBot, args(ModelNumber, size,)) for size in SizeList for n in range(ThreadCount)]
for t in threads: t.start()'''