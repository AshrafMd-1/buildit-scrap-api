import requests
from bs4 import BeautifulSoup


def app_login(username_f, password_f):
    url = "http://buildit.iare.ac.in/login_"
    s = requests.Session()
    payload = {
        "username": username_f,
        "password": password_f
    }
    response = s.post(url, data=payload)
    u = response.text
    return s, u


def error_login(u):
    soup = BeautifulSoup(u, "html.parser")
    full_error = soup.select("body > section.page-title.bg-primary.position-relative > div > div > div > h1")[0]
    return full_error.text


def check_login(session, url):
    response = requests.get(url, cookies=session)
    redirects = response.history
    if len(redirects) == 0:
        return True
    else:
        return False
