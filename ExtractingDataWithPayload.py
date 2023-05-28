import requests
import csv
from bs4 import BeautifulSoup as BS

# Define the years for which you want to fetch data
Years = ["2020","2021","2022"]

# Base URL for the website
base_url = "https://vahan.parivahan.gov.in/vahan4dashboard/vahan/vahan/view/reportview.xhtml"

# Create a dataset list to store the extracted data
# Set request headers 
headers = {
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0",
"Accept": "application/xml, text/xml, */*; q=0.01",
"Accept-Language": "en-US,en;q=0.5",
"Accept-Encoding": "gzip, deflate, br",
"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
"Faces-Request": "partial/ajax",
"X-Requested-With": "XMLHttpRequest",
"Content-Length": "3566",

}

# Create a session object
session  = requests.Session()

# Create a dataset list to store the extracted data
dataset = [['Vehicle Class', '4WIC', 'LMV' ,'MMV', 'HMV', 'TOTAL', 'Year']]


# Iterate over each year
for year in Years:
	
	# Send a GET request to the base URL	
	get_response = session.get(base_url)
	soup1 = BS(get_response.content, 'html5lib')
	
	# Extract the ViewState value from the page
	view_state = soup1.find('input', {'name': 'javax.faces.ViewState'})['value']
	
	 # Construct the payload data for the POST request
	payload = {
    			"selectedYear_input": year,
    			"javax.faces.ViewState" :view_state,
    			"javax.faces.partial.ajax" : "true",
    			"javax.faces.source":"j_idt63",
    			"javax.faces.partial.execute": "@all",
    			"masterLayout_formlogin":"masterLayout_formlogin",
    			"vchgroupTable:selectCatgGrp_input":"4W|5,7,15,23,31,56,70,71,93|4WIC,LMV,MMV,HMV",
    			"yaxisVar_input":"Vehicle Class",
    			"xaxisVar_input":"VCG",
    			"selectedYearType_input":"C",
    			"j_idt24_input":"A",
    			"javax.faces.source":"j_idt63",
    			"javax.faces.partial.render":"VhCatg norms fuel VhClass combTablePnl groupingTable msg vhCatgPnl",
    			"j_idt63":"j_idt63",
    			"j_idt24_focus":	"",
			"j_idt33_focus":	"",
			"j_idt33_input":	"-1",
			"selectedRto_focus":	"",
			"selectedRto_input":	"-1",
			"yaxisVar_focus":	"",
			"xaxisVar_focus": "",
			"selectedYear_focus": "",
			"vchgroupTable_scrollState":	"0,0",
		}
		
	# Send a POST request to the base URL with the payload data	
	response = session.post(base_url, data=payload, headers=headers )
	
	
	#print(response.content)
	
	soup = BS(response.content, 'html5lib')
	#print(soup.prettify())
	
	
	 # Find the table data within the HTML
	table_data = soup.find('tbody', class_="ui-datatable-data ui-widget-content")
	
	rows = table_data.find_all('tr')

	# Extract the data from each row
	
	for row in rows:
    		cells = row.find_all('td')
    		row_data = [cell.get_text(strip=True) for cell in cells[1:] ]
    		row_data.append(year)
    		dataset.append(row_data)
	
	
	#print(dataset)

# Write the dataset to a CSV file
with open("vahaan_data.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(dataset)
    
print(f'Successfully saved the news articles to vahaan_data.csv.')

	
	
