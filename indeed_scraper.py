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


if __name__ == "__main__":
      
    # Data for URL
    job = "data+scientist"
    Location = "Vancouver%2C+BC"
    time = "7"
    url = "https://ca.indeed.com/jobs?q="+job+"&l="+Location+"&fromage="+time
  
    soup = html_code(url)

    job_res = job_data(soup)
    com_res = company_data(soup)
    location_res = location_data(soup)
  
    for x in range(len(job_res)):
        print(f"Job Title: {job_res[x]} \n")
        print(f"Company Name: {com_res[x]} \n")
        print(f"Location: {location_res[x]} \n")
        print("--------------------------------------")

# printing length of results for debug
    print(len(job_res))
    print(len(com_res))
    print(len(location_res))

