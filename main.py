import string
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
    data_str = ""
    for item in soup.find_all("a", class_="jcs-JobTitle"):
        data_str = data_str + "/n" + item.get_text()
    result = data_str.split("/n")

    res = []
    for i in result:
        if len(i) > 1:
            res.append(i)
    return res


if __name__ == "__main__":
    job = "data+scientist"
    Location = "Vancouver%2C+BC"
    start = 40

    url = "https://ca.indeed.com/jobs?q="+job+"&l="+Location+"&sort=date&start="+str(start)
    soup = html_code(url)

    print(len(job_data(soup)))