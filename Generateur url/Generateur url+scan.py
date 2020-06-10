# Base URL =  https://www.zalando.fr/nike-sportswear-air-force-1-07-an20-baskets-basses-whiteblack-ni112o0cl-a11.html
# Base URL = https://www.zalando.fr/nike-sportswear-air-max-2090-baskets-basses-whiteblackpure-platinumbright-crimsonwolf-greyblue-hero-ni112o0cd-a11.html
#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def URLGen(model, ref, coul, type_):
	
	URL = 'https://www.zalando.fr/' + str(type_)+ "-" + str(model) + "-" + str(coul) + "-" + str(ref) + ".html"
	return URL


type_ = input ("Entrer le type de produit :")
type_= type_.lower()
type_= type_.replace(" ", "-")

Model = input('Model #: ')
Model = Model.lower()
Model= Model.replace("’","")
Model= Model.replace("  "," ")
Model= Model.replace(" - ","-")
Model= Model.replace(" ","-")

reference = input('Reference : ')
reference= reference.lower()

couleur= input( "couleur :")
couleur= couleur.replace("/", "")



URL = URLGen(Model, reference, couleur, type_)


print(URL)
