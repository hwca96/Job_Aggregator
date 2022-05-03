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
    for i in range(1, len(result)):
        if len(result[i]) > 1:
            res.append(result[i])
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

if __name__ == "__main__":
    job_res = []
    com_res = []
    location_res = []
    posted_res = []
    url_res = []
      
    # Data for URL
    # Default values for now
    # TODO
    job = "data+scientist"
    Location = "Vancouver%2C+BC"
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
        if "30+ days" in posted_res[-1]:
            break
        start += 10
  
    for x in range(len(job_res)):
        print(f"Job Title: {job_res[x]} \n")
        print(f"Company Name: {com_res[x]} \n")
        print(f"Location: {location_res[x]} \n")
        print(f"Posted: {posted_res[x]} \n")
        print(f"URL: {url_res[x]} \n")
        print("--------------------------------------")

# printing length of results for debug
    print(len(job_res))
    print(len(com_res))
    print(len(location_res))
    print(len(posted_res))
    print(len(url_res))

