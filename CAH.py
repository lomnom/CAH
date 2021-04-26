import FUNC as f
from sys import argv
import os
import shutil

f.log("reading file")

decks=f.readYaml("CAH.yaml")

f.log("read file")

f.log("decks:")
for n in range(len(decks)):
	f.log(str(n)+": "+decks[n]["name"])

deckId=int(input("deck? "))
deckName=decks[deckId]["name"]
path="cards/"+deckName+"/"
try:
	os.mkdir(path)
except:
	try:
		os.mkdir("cards")
		os.mkdir(path)
	except:
		shutil.rmtree(path)
		os.mkdir(path)
deck=decks[deckId]

deckWhite=deck["white"]
deckBlack=deck["black"]

whiteCards=[]

for card in deckWhite:
	whiteCards+=[card["text"]]

blackCards=[]

for card in deckBlack:
	blackCards+=[[card["text"],card["pick"]]]

f.log("made decks")

blacks=len(blackCards)
whites=len(whiteCards)

f.log("length of white deck is "+str(whites))
f.log("length of black deck is "+str(blacks))

default=f.read("RESCOURCES/WHITECARD.svg")

f.log("read svg")

for i in range(len(whiteCards)):
	svg=default
	text=f.splitStringWithDash(
		whiteCards[i],20
	)

	f.log("card: "+whiteCards[int(i)])

	f.log("text: "+str(text))

	locations=["Ѹ","Ψ","Ѻ","Ө","ӿ","ʨ","~","Ϟ","ʬ"]

	for n in range(len(text)):
		svg=svg.replace(locations[n],text[n].replace("&","&amp;").replace(">","&gt;").replace("<","&lt;"))

	for location in locations:
		svg=svg.replace(location,"")

	f.write(path+"WHITE"+str(i)+".svg",svg)
	f.log("wrote svg "+str(i+1)+"/"+str(whites))

f.log("processing black cards")
blackText=[]
for i in range(len(blackCards)):
	if blackCards[i][1]==2:
		blackText+=["Draw 2."]
	else:
		blackText+=[""]
	blackCards[i]=blackCards[i][0]
f.log("processed")

f.log("reading svg")
default=f.read("RESCOURCES/BLACKCARD.svg")
f.log("read svg")

for i in range(len(blackCards)):
	svg=default
	text=f.splitStringWithDash(
		blackCards[i],20
	)

	if len(text)==8:
		text=text+[blackText[i]]
	else:
		text=text+[" ",blackText[i]]

	f.log("card: "+blackCards[int(i)])

	f.log("text: "+str(text))

	locations=["Ѹ","Ψ","Ѻ","Ө","ӿ","ʨ","~","Ϟ","ʬ"]

	for n in range(len(text)):
		if not text[n]=="":
			svg=svg.replace(locations[n],text[n].replace("&","&amp;").replace(">","&gt;").replace("<","&lt;"))

	for location in locations:
		svg=svg.replace(location,"")

	f.write(path+"BLACK"+str(i)+".svg",svg)

	f.log("wrote svg "+str(i+1)+"/"+str(blacks))


f.log("converting files into pdf")
import cairosvg
import os

f.log("converting white cards into png")

def toPdf(inFile,outFile,remove=True):
	cairosvg.svg2pdf(
		file_obj=open(inFile, "rb"), write_to=outFile)
	if remove:
		os.remove(inFile)

for i in range(len(whiteCards)):
	f.log("converting "+str(i))
	toPdf(path+"WHITE"+str(i)+".svg",path+"WHITE"+str(i)+".pdf")

f.log("conversion done")

f.log("merging all white cards")
from PyPDF2 import PdfFileMerger, PdfFileReader
 
mergedObject = PdfFileMerger()

for i in range(len(whiteCards)):
	f.log("merging "+str(i))
	mergedObject.append(PdfFileReader(path+"WHITE"+str(i)+'.pdf', 'rb'))
	os.remove(path+"WHITE"+str(i)+'.pdf')
f.log("saving...")
mergedObject.write(path+"WHITE.pdf")
f.log("merged all white")

for i in range(len(blackCards)):
	f.log("converting "+str(i))
	toPdf(path+"BLACK"+str(i)+".svg",path+"BLACK"+str(i)+".pdf")

f.log("conversion done")

f.log("merging black cards")
 
mergedObject = PdfFileMerger()

for i in range(len(blackCards)):
	f.log("merging "+str(i))
	mergedObject.append(PdfFileReader(path+"BLACK"+str(i)+'.pdf', 'rb'))
	os.remove(path+"BLACK"+str(i)+'.pdf')

f.log("saving...")
mergedObject.write(path+"BLACK.pdf")

f.log("merged black")
f.log("merging white and black")

mergedCards = PdfFileMerger()

mergedCards.append(PdfFileReader(path+"BLACK.pdf", 'rb'))
mergedCards.append(PdfFileReader(path+"WHITE.pdf", 'rb'))

mergedCards.write(path+"CARDS.pdf")
f.log("merged all cards")
f.log("converting and merging rules")
toPdf("RESCOURCES/RULES1.svg",path+"RULES1.pdf",remove=False)
toPdf("RESCOURCES/RULES2.svg",path+"RULES2.pdf",remove=False)

mergedObject = PdfFileMerger()
mergedObject.append(PdfFileReader(path+"RULES1.pdf", 'rb'))
mergedObject.append(PdfFileReader(path+"RULES2.pdf", 'rb'))

os.remove(path+"RULES1.pdf")
os.remove(path+"RULES2.pdf")
mergedObject.write(path+"RULES.pdf")
f.log("done")

f.log("merging and writing cards with rules")
mergedCards.append(PdfFileReader(path+"RULES.pdf", 'rb'))
mergedCards.write(path+"CARDSWITHRULES.pdf")
f.log("done")
