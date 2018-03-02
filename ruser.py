uList = {}
d = ''
#DATA MUST STAY ON FIRST TWO LINES. DO NOT MODIFY.

import sys


#Functions

def setUser(rname):  ## FUNC: To be called when imported, set which user data to use
	global uDict
	uDict ={"client_id":uList[rname][0], "client_secret":uList[rname][1], "password":uList[rname][2], "user_agent":"script", "username":rname}

def configure(): ## FUNC: replace location called with reddit script. Do not call within itself.
	if __name__ == '__main__': return
	import __main__
	with open(__main__.__file__, 'r') as f:
		file = f.readlines()
	fp = open(__main__.__file__, 'w')
	index = -1
	rString = "praw.Reddit(**{}.uDict)".format(__name__)
	confString = "{}.configure()".format(__name__)
	for line in file:
		index += 1
		if not line.find(confString) == -1:  ### Checks if ruser.configure() is in string
			file[index] = line.replace(confString, rString)  ### if it is, it replaces it with the correct configuration.
	fp.writelines(file)
	fp.close
	print("[ruser]:SCRIPT CONFIGURED")
	sys.exit()

setUser(d)

	
#--------INTERNAL FUNCTIONS---------------#
# These are used when configuring.        #  
# They exporting to min will remove them. #
#-----------------------------------------#

import os.path
import praw
from pprint import pprint
	
def commandRead(comRaw): ## FUNC: Process user input from main command area.
	com = comRaw.lower()
	if com == "ls":
		lsName()
	elif com.startswith("add"):
		addName(parseArgs(com, "add"))
	elif com.startswith("cp"):
		cpName(parseArgs(com, "cp"))
	elif com.startswith("rm"):
		rmName(parseArgs(com, "rm"))
	elif com.startswith("mod"):
		modName(parseArgs(com, "mod"))
	elif com.startswith("def"):
		setDef(parseArgs(com, "def"))
	elif com == "x" or com == "exit":
		global lock
		global rr
		lock = False  ### Disable the run lock state
		rr = False  ### reset restart recommendation
	elif com == "?" or com == "help":
		prHelp() ### Display Help Commands
	elif com.startswith("lf"):
		loc = parseLoc(com, 1)
		if loc: loadFile(loc)  ### Overwrite all data with data from file
	elif com.startswith("if"): 
		loc = parseLoc(com, 1)
		if loc: loadFile(loc, True)  ### import data from file
	elif com.startswith("sf"): 
		loc = parseLoc(com, 2)
		if loc: saveFile(loc)  ### save user data to file
	elif com == "exp":
		exportScript()
	elif com.startswith("acc"):
		modAcc(*com.split()[1:])
	elif com == "cldata":
		clearData()
	else:
		print("invalid command")
	
	


def parseArgs(com, cName): ##FUNC: Check for arguments
	if com == cName:
		return None
	elif len(com.split()) == 2:
		return com.split()[1]

def parseLoc(com, checkExist=0): ##FUNC: Get Location
	if len(com.split()) != 2:
		loc = input("Location:\n >")
	else:
		loc = com.split()[1]
	exist = os.path.isfile(loc)
	if checkExist == 0:
		return loc
	elif checkExist == 1:
		if exist: return loc
		else:
			print("Path not found")
			return False
	else:
		if not exist: return loc
		else:
			if input("File {loc} already exists. Overwrite? (y/n)\n >").lower == "y": return loc
			return False
	
def getName(name):  ##FUNC: Check if name is set, if not, set a name.
	if name != None:
		return name
	else:
		lsName()
		return input("select user:\n>").lower() or d
	
def prHelp():  ## COMMAND:[?]: Print Help Message
	print("+-HELP-------------------------+")
	print("| ls - List users              |")
	print("| add - add user               |")
	print("| cp - duplicate user          |")
	print("| rm - remove user             |")
	print("| mod - modify user            |")
	print("| def - set default user       |")
	print("| sf - save all data to file   |")
	print("| lf - load all data from file |")
	print("|  (remove all current data)   |")
	print("| if - import data from file   |")
	print("|  (does not remove current)   |")
	print("| exp - export to small script |")
	print("| acc - accept mod invite      |")
	print("| x - exit                     |")
	print("| ? - view this message        |")
	print("+------------------------------+\n")
	
def addName(name=None, init=False):   ## COMMAND:[add]: Add User to list
	mList = uList
	if name != None:
		nName = name
		print("reddit username:\n >{}")
	else:
		lsName()
		nName = input("reddit username:\n >").lower()
	nPW = input("reddit password:\n >")
	nID = input("app id:\n >")
	nSec = input("app secret:\n >")
	mList[nName] = [nID, nSec, nPW]
	dWrite(mList)
	return nName
	
def cpName(name=None):
	mList = uList
	sName = getName(name)
	nName = input("copy settings from '{}' to\n >".format(sName))
	mList[nName] = mList[sName]
	dWrite(mList)
	
def lsName():   ## COMMAND:[ls]: List all saved users
	for name in uList.keys():
		if name == d:
			print(name + " - DEFAULT")
		else:
			print(name)
	
def modName(name=None):  ## COMMAND:[mod]: Change settings on Users
	mList = uList
	sName = getName(name)
	mData = mList[sName]
	print("modifying user '{}'".format(sName))
	print("hit [enter] to skip value")
	inpTemp = input("Password\n  Current: [{}] -> ".format(mData[2]))
	mData[2] = inpTemp or mData[2] ### if inpTemp is empty, use previous value
	inpTemp = input("Client ID\n  Current: [{}] -> ".format(mData[0]))
	mData[0] = inpTemp or mData[0]
	inpTemp = input("Client Secret Key\n  Current: [{}] -> ".format(mData[1]))
	mData[1] = inpTemp or mData[1]
	mList[sName] = mData
	if input("Change Username? (y/N)").lower() == 'y':
		newName = input("Name\n Current: [{}] ->".format(sName)).lower() or sName
		if newName != sName:
			mList[newName] = mList.pop(sName)  #duplicates data to a new key, removes old key
			global d
			if d == sName:
				d = newName
				setDef(newName)
	dWrite(mList)
	
def rmName(name=None):  ## COMMAND:[rm]: Remove a user from the data set
	mList = uList
	sName = getName(name)
	del mList[sName]
	dWrite(mList)

def setDef(name=None):  ## COMMAND:[def]: Set default user
	sName = getName(name)
	print("setting {} as default user".format(sName))
	global d
	d = sName
	dWrite("'{}'".format(sName), 1)
	
def loadFile(loc, modify=False):  ## COMMAND:[lf]: Load data from file, and either modify/add users accordingly (when modify passed as True) or entirely replace them. Unlisted
	with open(loc) as f:
		fData = f.readlines() ### read the data file 
	mList = {}
	default = ''
	sdef = False
	if modify: mList = uList ### if modify is true, load current data
	for dLine in fData:
		dLine = dLine.rstrip()  ### remove trailing whitespace
		if (not dLine.startswith("#")) and (len(dLine.split()) > 3): ### filter out incomplete lines and comments
			data = dLine.split()
			mList[data[0]] = [data[2], data[3], data[1]]
			if default == '' and not modify: default = data[0] ### set to default if default is blank
			if len(data) == 5 and data[4].lower() == "default": default = data[0]  ### check if data in file indicates as default
	dWrite(mList)   ### save data to script
	if not default == '': setDef(default)
	
def saveFile(loc=None):   ## COMMAND:[sf]: Save data to file
	sf = open(loc, 'w')
	for user in uList.keys():
		str = "{} {} {} {}".format(user, uList[user][2], uList[user][0], uList[user][1])
		if user == d:
			str += " default"  ### if user is the default, mark as such
		str += "\n"
		print("saving '{}'...".format(user))
		sf.write(str)
	sf.close
	print("\nsaved to '{}'".format(loc))
	
def modAcc(name=None, sub=None): ## COMMAND:[mod]: Accept mod invite
	modName = getName(name)
	if sub is None:
		sub = input("subreddit: /r/")
	setUser(modName)
	rInstance = praw.Reddit(**uDict)
	print(f"logging in as {rInstance.user.me()}...")
	try:
		rInstance.subreddit(sub).mod.accept_invite()
	except Exception as e:
		err = type(e).__module__ + '.' + type(e).__name__		
		if err == "praw.exceptions.APIException":
			print("\n[!] Error: Are you sure you are invited?")
			print(f"PRAW Error: {e.args}")
		else:
			print(f"[!] Error: {err}")
	else:
		print(f"Invite to mod /r/{sub} accepted.")
	
def exportScript(): ## COMMAND:[exp]: Export to minimal script
	if rr:
		print("\nrestart required before export")
		return
	with open(__file__, 'r') as f:
		fs = f.readlines()
	f = open("ruser_min.py", 'w')
	f.writelines(fs[:33])
	f.close()
	print("exported to 'ruser_min.py'")

def clearData(): ## COMMAND:[cldata]: Clear all data
		uList = {}
		d = ''
		dWrite(uList)
		dWrite(d, 1)
		print("Data cleared")
		global lock 
		global rr
		rr = False
		lock = False
		
def dWrite(rawdata, line=0):   ## FUNC: Write data to script
	if line == 0:
		global uList
		uList = rawdata
	prefix = ("uList = ", "d = ")
	data = str(rawdata)
	with open(__file__, 'r') as f:
		file = f.readlines()
	fp = open(__file__, 'w')
	file[line] = "{}{}\n".format(prefix[line],data)
	fp.writelines(file)
	fp.close
	global rr
	rr = True


	


#---------RUN ONLY IF SCRIPT IS THE ONE RUNNING---------#
if __name__ == '__main__':
	lock = True
	rr = False
	if len(uList) < 1: ### Check if there is data, if not, run initial
		setDef(addName())
		print("\n\n\ninitial setup complete. run again to adjust configuration")
		quit()
	prHelp()
	while lock:
		commandRead(input("\n>"))
		if rr: print("script restart recommended")
