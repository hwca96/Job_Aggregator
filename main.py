

from datetime import date, datetime


if __name__ == "__main__":
    posted = datetime.strptime("January 10, 2022", "%B %d, %Y")
    now = datetime.now()

    print((now - posted).days)