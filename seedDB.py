import os
import json
path = "mtg5/json"
files =  os.listdir(path)
s= "["
i = 1
for file in files:
	print(file)
	st = file.split(".")[0]
	with open(path+"/"+file) as data_file:    
		data = json.load(data_file)
	for item in data["cards"]:
		s+= "{\"fields\": {\"name\": \"" + item["name"] + "\",  \"setName\":\""+ st + "\", \"number\": " +item["number"] +"}, \"model\": \"mtg5.card\", \"pk\": " + str(i) + "}, "
		i=i+1
s += "]"
f = open('standard.json', 'w')
f.write(s.encode('utf8'))
f.close()
