from datetime import datetime
from tokenize import String
from unittest import result
from pip import main
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
    temp = []
    res = []
    data_str = ""
    for item in soup.find_all("span", class_ = "noctitle"):
        [temp.append(text) for text in item.stripped_strings]

    for s in temp:
        if s != "Verified" and not s.startswith("This job"):
            res.append(s)

    return res

def company_data(soup):
    res = []
    for item in soup.find_all("li", class_="business"):
        res.append(item.get_text())
    return res

def location_data(soup):
    temp = []
    res = []
    for item in soup.find_all("li", class_="location"):
        [temp.append(text) for text in item.stripped_strings]

    for s in temp:
        if s != "Location":
            res.append(s)
    return res

def job_url_data(soup):
    res = []
    for item in soup.find_all("a", class_="resultJobItem"):
        res.append("https://www.jobbank.gc.ca"+item['href'])
    return res

def posted_data(soup):
    res = []
    for item in soup.find_all("li", class_="date"):
        temp = datetime.strptime(item.get_text().strip(), "%B %d, %Y")
        posted = (datetime.now() - temp).days
        res.append(posted)
    return res

def result_number(soup):
    res = []
    for item in soup.find_all("span", class_="found"):
        res.append(int(item.get_text()))
    return res[0]

def get_job_list(job_name: str, job_location: str):
    job_list = []
    job_name = "cashier"
    job_location = "Vancouver"
    page = 1

    base_url = f"https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring={job_name}&locationstring={job_location}&sort=D&page={page}"
    base_soup = html_code(base_url)
    found = result_number(base_soup)

    if found == 0:
        print("None Found")
    else:
        while len(job_list) < found:
            url = f"https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring={job_name}&locationstring={job_location}&sort=D&page={page}"
            soup = html_code(url)

            job_res = job_data(soup)
            company_res = company_data(soup)
            location_res = location_data(soup)
            url_res = job_url_data(soup)
            posted_res = posted_data(soup)

            page += 1

            for x in range(len(job_res)):
                job = Job(job_res[x], company_res[x], location_res[x], url_res[x], posted_res[x])
                job_list.append(job)
    return job_list

if __name__ == "__main__":
    jobs = get_job_list("cashier", "Vancouver")

    for x in jobs:
        print(x)
        print("----------------------")
