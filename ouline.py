#import beautifulsoup and request here
from urllib import response
from bs4 import BeautifulSoup;
from flask import Flask, render_template;

import requests;
import json;

app = Flask(__name__)
@app.route("/")
def displayJobDetails():
    
    #write a code to give call to json file and then render html page
    response = requests.get('https://raw.githubusercontent.com/Jsalasay/pythonBeautifulSoup/main/jobDetails.json')
    #responseJSON = json.loads(json.dumps(response.json()))
    responseJSON = json.loads(response.text)
    return render_template('index.html',responseJSON = responseJSON)


def displayJobDetails(jobResult):
    #data output
    print("====JOB FOUND====")
    print("Title: %s\nCompany: %s\nSalary: %s\nDescription:" % (jobResult['title'], jobResult['company'], jobResult['salary']))
    for subDesc in jobResult['description']:
        print("\t-%s" % subDesc)
    print("\n")

#function to get job list from url 'https://www.indeed.com/jobs?q={role}&l={location}'
def getJobList(role,location):
    url = ('https://www.indeed.com/jobs?q=%s&l=%s' % (role, location))
    
    #response = requests.request("GET", url, headers = {}, data = {})
    response = requests.get(url)
    htmlDoc = response.text
    soup = BeautifulSoup(htmlDoc, 'html.parser')
    jobList = []

    for jobResult in soup.find_all(class_ = "result"):
        #wrappers
        descriptionWrapper = jobResult.find('div', class_ = "job-snippet")
        dirtiedDescriptionWrapper = descriptionWrapper.find_all('li')
        titleWrapper = jobResult.find('h2', class_ = 'jobTitle')
        companyWrapper = jobResult.find('span', class_ = 'companyName')
        salaryWrapper = jobResult.find('div', class_ = 'salary-snippet-container')

        #extracted data
        title = titleWrapper.text if (titleWrapper != None) else "N/A"
        company = companyWrapper.text if (companyWrapper != None) else "N/A"
        salary = salaryWrapper.text if (salaryWrapper != None) else "N/A"
        description = []

        #data cleanup
        if title[:3] == "new":
            title = title[3:]

        for subDescription in dirtiedDescriptionWrapper:
            description.append(subDescription.text)

        #data packing
        job = {
            "title": title,
            "company": company,
            "salary": salary,
            "description": description
        }
        jobList.append(job)

    return jobList


#save data in JSON file
def saveDataInJSON(jobDetails):
    outFile = open('jobDetails.json', 'w')
    json.dump(jobDetails, outFile)
    print("Saving data to JSON")
    outFile.close()

#main function
def main():
    print("Enter role you want to search")
    role = input()
    print("Enter location")
    location = input()
    print('Role" %s, Location: %s \n'%(role,location))

    jobList = getJobList(role,location)
    saveDataInJSON(jobList)
    for job in jobList:
        displayJobDetails(job)
    
if __name__ == '__main__':
    app.run(host='127.0.01', port=8000, debug=True)
    displayJobDetails()
