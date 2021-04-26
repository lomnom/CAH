def randomCase(s):
    result = ''
    for c in s:
        case = random.randint(0, 1)
        if case == 0:
            result += c.upper()
        else:
            result += c.lower()
    return result

from datetime import datetime
def log(message): #define logging function to prevent repeated code
    currentTime = str(datetime.now().time())
    print("["+currentTime+"] "+message)

def read(file):#read file function
	with open(file) as content: #save save slot
		return content.read()

def write(file,data): #function to write to file
	with open(file, 'w') as content: #save save slot
		content.write(str(data))
		return True

def exists(file):#read file function
	try: #load slot
		with open(file) as content: #save save slot
			return True
	except OSError:
		return False

def readWithBackup(file,backup):#read file function
	try: #load slot
		with open(file) as content: #save save slot
			return content.read()
	except OSError:
		write(file,backup)
		return backup

from yaml import full_load, dump
def readYaml(fileName):
	return full_load(read(fileName))

def writeYaml(fileName,data):
	return write(fileName,dump(data,allow_unicode=True))

from json import loads
def readJson(fileName):
	return loads(read(fileName))

def splitString(string,n):
    chunks = [string[i:i+n] for i in range(0, len(string), n)]
    return chunks

def endsWithAny(possibilities,string):
    for possibility in possibilities:
        if string.endswith(possibility):
            return True
    return False

def splitStringWithDash(string,n):
    n-=1
    chunks = [string[i:i+n] for i in range(0, len(string), n)]
    if not len(chunks)==1:
        for i in range(len(chunks)):
            if len(chunks[i])==n and not endsWithAny(["."," ","!","?","\""],chunks[i]):
                chunks[i]=chunks[i]+"-"
    for i in range(len(chunks)):
        if chunks[i].startswith(" "):
            chunks[i]=withoutFirstChar(chunks[i])
    return chunks

def withoutFirstChar(string):
    return string[1:]

def splitIgnoreWords(string,n): #split str into n chunks 
    words=string.split(" ")
    temp=""
    chunks=[]
    for word in words:
        if len(temp+word)>n:
            chunks.append(temp)
            temp=""
        temp+=word+" "
    chunks.append(temp)
    return chunks