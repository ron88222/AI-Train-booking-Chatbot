import requests
import json

# Documentation can be found at
#   https://wiki.openraildata.com/index.php/HSP

# When registering at https://datafeeds.nationalrail.co.uk/
# you only need the HSP subscription
# The Real time Data feed is too much to deal with
# The On Demand Data Feeds might be useful
# 
# In 'Planned usage', mention you are using the HSP data 
# for educational purposes, for a project, and for a limited
# time
# The T & Cs should not be an issue, nor the limit on the
# number of requests an hour - but do be polite and do not
# swamp the web service with an excessive number of requests

def getMetrics(r):
	results = r.json()
	services = results.get("Services")
	header = results.get("header")

	#results: dictionary
	#services: list
	
	# Metrics

	o_locList = []
	d_locList = []
	dep_time = []
	arr_time = []
	dates = []

	for service in services:
		#service: dictionary
		serviceAttributesMetrics = service.get("serviceAttributesMetrics") #sAM: dictionary
		o_locList.append(serviceAttributesMetrics.get("origin_location"))
		d_locList.append(serviceAttributesMetrics.get("destination_location"))
		dep_time.append(serviceAttributesMetrics.get("gbtt_pta"))
		arr_time.append(serviceAttributesMetrics.get("gbtt_ptd"))
		dates.append(serviceAttributesMetrics.get("rids"))

		# metrics = service.get("Metrics")[0] #metrics:dictionary
		#Metrics: {'tolerance_value': '0', 'num_not_tolerance': '1', 'num_tolerance': '4', 'percent_tolerance': '80', 'global_tolerance': True}
		#ServiceAttributesMetrics: {'origin_location': 'NRW', 'destination_location': 'LST', 'gbtt_ptd': '0700', 'gbtt_pta': '0855', 'toc_code': 'LE', 'matched_services': '5', 'rids': ['201607023392291', '201607093593592', '201607163804077', '201607234018314', '201607304230564']}

	# n = 0
	# while n < len(o_locList):
	# 	print(o_locList[n])
	# 	print(d_locList[n])
	# 	print(dep_time[n])
	# 	print(arr_time[n])
	# 	print(dates[n],"\n")
	# 	n+=1;

	return [o_locList,d_locList,dep_time,arr_time,dates]


def getDetails(r):
	results = r.json()

	r = str(results).replace("{","\n")
	print(r)
	return

	print(results)
	print()
	sad = results["serviceAttributesDetails"]
	print(sad["locations"])

	return

def exportCSV(data, filename):
	print("Exporting...")

	with open(filename, 'w') as file:

		#n = index
		n = 0
		m = 0
		while n < len(data[0]):
			if(m!=len(data[0])-1):
				file.write(data[m][n])
				file.write(",")
				print(data[m][n])
			else:
				times = str(data[m][n])
				file.write(times)
				print(times)
			m+=1
			if(m==len(data[0]) and n!=len(data[0])):
				m=0
				n+=1
				file.write("\n")
				print()

	print("Finished exporting.")




def main():
	print("Hii")
	mode = "metrics"

	if(mode=="metrics"):
		api_url = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
	elif(mode=="details"):
		api_url = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"
	else:
		print("Please change 'mode' variable")
		return

	headers = { "Content-Type": "application/json" }
	auths = ("acc16scu@uea.ac.uk", "Ronis1337!")

	from_loc = "NRW"
	to_loc = "CBG"
	from_time = "0700"
	to_time = "0900"
	from_date = "2016-07-01"
	to_date = "2016-08-01"
	days = "SATURDAY"

	data = {
	  "from_loc": from_loc,
	  "to_loc": to_loc,
	  "from_time": from_time,
	  "to_time": to_time,
	  "from_date": from_date,
	  "to_date": to_date,
	  "days": days
	}

	filename = from_loc + "_" + to_loc + "_" + days[0:3].lower() + ".csv"

	r = requests.post(api_url, headers=headers, auth=auths, json=data)
	# r = requests.get(api_url, headers=headers, auth=auths, json=data)
	
	#Method to retrieve the relevant data
		#Returns a list of the required metrics
	metricResults = getMetrics(r)
	print(metricResults)
	#Outputs the retrieved data into a custom CSV file
	exportCSV(metricResults,filename)

	##Service details
	api_url = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"

	data = {"rid": 0}
	
	# detailsResults = getDetails(metricResults[4])
	for a in metricResults[4]:
		for b in a:
			data["rid"] = b
			r = requests.post(api_url, headers=headers, auth=auths, json=data)
			getDetails(r)
			return
			# print(json.dumps(json.loads(r.text), sort_keys=True, indent=2, separators=(',',': ')))
	return
	
	
	

	# print(json.dumps(json.loads(r.text), sort_keys=True, indent=2, separators=(',',': ')))
	
	print("Fin")
    

if __name__ == '__main__':
   main()
