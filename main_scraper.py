import indeed_scraper, jobbank_scraper


def sort_date(job_list):
    job_list.sort(key=lambda j: j.posted)

def filter_source(job_list, source:str):
    res = []
    for x in job_list:
        if x.source == source:
            res.append(x)
    return res

def get_all_data(job_title, location):
    data = indeed_scraper.get_job_list(job_title, location)
    data.extend(jobbank_scraper.get_job_list(job_title, location))
    sort_date(data)
    return data

if __name__ == "__main__":
    job_title = "junior software"
    location = "Vancouver, BC"
    data = indeed_scraper.get_job_list(job_title, location)
    data.extend(jobbank_scraper.get_job_list(job_title, location))

    sort_date(data)

    indeed = filter_source(data, "indeed")

    for x in indeed:
        print(x)
        print("----------------------------")