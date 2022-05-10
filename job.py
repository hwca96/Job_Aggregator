class Job:
    def __init__(self, title, company, location, url, posted):
        self.title = title
        self.company = company
        self.location = location
        self.url = url
        self.posted = posted

    def __repr__(self):
        return f"Job Title: {self.title}\nCompany Name: {self.company}\nLocation: {self.location}\nPosted: {self.posted} Days Ago\nURL: {self.url}"
