import requests
from bs4 import BeautifulSoup

from job import Job

def getData(url):
    req = requests.get(url)
    return req.text

def html_code(url):
    htmldata = getData(url)
    soup = BeautifulSoup(htmldata, "html.parser")

    return soup

def job_data(soup):
    data_str = ""
    for item in soup.find_all("a", class_="jcs-JobTitle"):
        data_str = data_str + "/n" + item.get_text()
    result = data_str.split("/n")

    res = []
    for i in result:
        if len(i) > 1:
            res.append(i)
    return res

def company_data(soup):
    data_str = ""
    for item in soup.find_all("span", class_="companyName"):
        data_str = data_str + "/n" + item.get_text()
    result = data_str.split("/n")

    res = []
    for i in range(1, len(result)):
        if len(result[i]) > 1:
            res.append(result[i])
    return res

def location_data(soup):
    data_str = ""
    for item in soup.find_all("div", class_="companyLocation"):
        data_str = data_str + "/n" + item.get_text()
    result = data_str.split("/n")

    res = []
    for i in range(1, len(result)):
        if len(result[i]) > 1:
            res.append(result[i])
    return res


def posted_data(soup):
    data_str = ""
    for item in soup.find_all("span", class_="date"):
        data_str = data_str + "/n" + item.get_text()[6:]
    result = data_str.split("/n")

    res = []
    for i in result:
        if len(i) > 1:
            if "Just posted" in i or "Today" in i:
                res.append(1)
            elif "30+" in i:
                res.append(30)
            elif "Active" in i:
                res.append(int(i.split(' ')[1]))
            else:
                res.append(int(i.split(' ')[0]))
    return res

def job_url_data(soup):
    data_str = ""
    for item in soup.find_all("a", class_="jcs-JobTitle"):
        data_str = data_str + "/n" + "https://ca.indeed.com"+ item['href']
    result = data_str.split("/n")

    res = []
    for i in result:
        if len(i) > 1:
            res.append(i)
    return res

def get_job_list(job_name: str, job_location: str):
    job_res = []
    com_res = []
    location_res = []
    posted_res = []
    url_res = []

    job_list = []

    # Data for URL
    job = job_name
    Location = job_location
    start = 0

    while True:
        retrieved = False
        
        while not retrieved:
            url = "https://ca.indeed.com/jobs?q="+job+"&l="+Location+"&sort=date&start="+str(start)
            soup = html_code(url)

            job_res_t = job_data(soup)
            com_res_t = company_data(soup)
            location_res_t = location_data(soup)
            posted_res_t = posted_data(soup)
            url_res_t = job_url_data(soup)

            if (len(job_res_t) != 0 and len(com_res_t) != 0 and len(location_res_t) != 0 and len(posted_res_t) != 0 and len(url_res_t) != 0):
                job_res.extend(job_res_t)
                com_res.extend(com_res_t)
                location_res.extend(location_res_t)
                posted_res.extend(posted_res_t)
                url_res.extend(url_res_t)
                retrieved = True
        
        # Avoid showing any jobs that are 30+ days old
        if posted_res[-1] == 30:
            break
        start += 10
  
    for x in range(len(job_res)):
        job = Job(job_res[x], com_res[x], location_res[x], url_res[x], posted_res[x], "indeed")
        job_list.append(job)

    return job_list

if __name__ == "__main__":
    jobs =  get_job_list("junior software", "Vancouver, BC")
    for x in jobs:
        print(x)
        print("------------------------------")


