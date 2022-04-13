#import beautifulsoup and request here
from bs4 import BeautifulSoup;
import requests;

def displayJobDetails(jobResult):
    print(1)
    #data output
    #print("====JOB FOUND====")
    #print("Title: %s\nCompany: %s\nSalary: %s\nDescription:\n%s" % (title, company, salary, description))

#function to get job list from url 'https://www.indeed.com/jobs?q={role}&l={location}'
def getJobList(role,location):
    url = ('https://www.indeed.com/jobs?q=%s&l=%s' % (role, location))
    
    response = requests.request("GET", url, headers = {}, data = {})
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
        description = ""

        #data cleanup
        if title[:3] == "new":
            title = title[3:]

        for subDescription in dirtiedDescriptionWrapper:
            description += ("\t-" + subDescription.text + "\n")

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
    #Complete the missing part of this function here
    print("Saving data to JSON")

#main function
def main():
    # Write a code here to get job location and role from user e.g. role = input()
    print("Enter role you want to search")
    role = input()
    print("Enter location you want to search")
    location = input()
    print('Role: %s, Location: %s' % (role, location))
    print("\n")
    
    jobList = getJobList(role, location);
    print(jobList)
    
if __name__ == '__main__':
    main()