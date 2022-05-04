from unittest import result
from pip import main
import requests
from bs4 import BeautifulSoup

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
        res.append(item['href'])
    return res

if __name__ == "__main__":
    url = "https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=cashier&locationstring=Vancouver%2C+BC&sort=D"
    soup = html_code(url)
    job_res = job_data(soup)
    company_res = company_data(soup)
    location_res = location_data(soup)
    print(job_url_data(soup))
