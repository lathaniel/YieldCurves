import requests, pprint
import json, xmltodict, re

def main():
    
    pp = pprint.PrettyPrinter()
      
    url = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/XmlView.aspx?data=yield'
    page = getPageText(url)
   
    pp.pprint(parseTreasuryXML(page))    

def getPageText(url):
    # intialize session
    session_requests = requests.session()

    # request the URL
    response = session_requests.get(url)

    return response.text

def parseTreasuryXML(s):
    # Dictionary to store yields
    yields = dict()

    # Parse xml page
    d = xmltodict.parse(s)

    # Loop through relevant data attributes
    for i in range(len(d["pre"]["entry"])):
        data = d["pre"]["entry"][i]["content"]["m:properties"]
        # Save each yield curve to a dictionary
        for key in data.keys():
            if 'date' in key.lower(): 
                date = re.search('([0-9]{4}-[0-9]{2}-[0-9]{2})', data[key]['#text'])[1]
                yields[date] = dict()
            elif 'bc' in key.lower():
                yields[date][re.sub('d:BC_', '',key)] = float(data[key]['#text'])
    return yields

if __name__=="__main__":
    main()