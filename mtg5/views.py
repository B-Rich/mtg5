from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.timezone import utc
from django.views.decorators.csrf import csrf_exempt
from mtg5.settings import STATIC_URL
from oauth2client.client import SignedJwtAssertionCredentials
import random, json, urllib, gspread, os
from mtg5.models import Card


def index(request):
	print("index")
	workbook = loadXLS()
	worksheet = workbook.worksheet("Red")
	players = worksheet.row_values(1)
	colors = list()
	wkshts = workbook.worksheets()
	i=0
	for item in wkshts:
		colors.append(str(item).split('\'')[1])
	colors.remove("Stats")
	
	#return users, colors
  	return render_to_response(
				'index.html',
				{
					'STATIC_URL':STATIC_URL,
					'players': sorted(players[2:-1]),
					'colors': sorted(colors)
				}
			)

def masterIndex():
	master = {
     'Colorless':[(2,36), (40,61),(65,81)],
	 'Multi':[(2,57),(61,70),(74,96)],
	 'Black':[(2,32),(36,66),(69,110),(115,158)],
 	 'Red':  [(2,33),(37,65),(69,110),(115,159)],
 	 'Green':[(2,33),(37,66),(71,113),(118,162)],
 	 'Blue': [(2,33),(37,65),(69,110),(115,158)],
 	 'White':[(2,32),(36,64),(68,109),(114,154)]
	}
	return master

def mapPlayerToCol(player):
	workbook = loadXLS()
	worksheet = workbook.worksheet("Red")
	users = worksheet.row_values(1)
	return users.index(player)+1


def getData(request,player,color):
	print("called")
	workbook = loadXLS()
	worksheet = workbook.worksheet(color)
	print("Getting names\n")
	playerID = mapPlayerToCol(player)
	allNames = worksheet.col_values(2)
	allCounts = worksheet.col_values(playerID)
	myNames = list()
	myCounts = list()
	myurls = list()
	index = masterIndex()
	imgurl = "http://magiccards.info/scans/en/"
	print("Sorting...")
	for rng in index[color]:
		myNames.extend(allNames[rng[0]-1:rng[1]-1])
		myCounts.extend(allCounts[rng[0]-1:rng[1]-1])
	i=0	
	while i<len(myCounts):
		print (i)
		if myCounts[i] is None:
			myNames.pop(i)
			myCounts.pop(i)
		else:
			print(myNames[i])
			card = Card.objects.filter(name=myNames[i])[0]
			set = card.setName
			number = card.number
			myurls.append(imgurl+set.lower()+"/"+str(number)+".jpg")
			i=i+1

	cards = zip(myNames,myCounts,myurls)
		
	return HttpResponse(json.dumps(cards))

def loadSheetAsList(sheetName):
	workbook = loadXLS()
	if (workbook):
		worksheet = workbook.worksheet(sheetName)
		worksheet_list = workbook.worksheets()
		list_of_lists = worksheet.get_all_values()
	return 'n'

def loadXLS():
	# Gather Oauth credentials
	json_key = json.load(os.environ['oauthkey'])
	scope = ['https://spreadsheets.google.com/feeds']
	credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
	gc = gspread.authorize(credentials)
	# Pull the workbook
	return gc.open("KoT_FR_Dragons of Tarkir League 0315")
