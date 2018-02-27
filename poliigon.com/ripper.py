import random
import string
import requests
import time
from guerrillamail import GuerrillaMailSession


proxies = {
    # 'https': 'https://##.##.##.##:##',
}


headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Referer": "https://www.poliigon.com/register",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}


def read_email(email):
    s = GuerrillaMailSession()

    s.set_email_address(email)

    print(s.get_session_state())

    for email in s.get_email_list():
        if email.subject == "Poliigon: Email Verification":
            print("Got email")

            body = s.get_email(s.get_email_list()[0].guid).body
            link = body[body.index("https://www.poliigon.com"):body.index("https://www.poliigon.com") + 71]

            return link


def download_file(url, cookies):

    r = requests.get(url, stream=True, headers=headers, proxies=proxies, cookies=cookies)

    if "X-Sendfile" in r.headers:
        local_filename = r.headers["X-Sendfile"].split('/')[-1]

        print(local_filename + "...")

        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return False
    else:

        print("Error")
        return True


def rand_string():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(12))


def get_next_num():
    counter_file = open("counter")
    counter = int(counter_file.read())

    counter_file.close()
    counter_file = open("counter", 'w')
    counter_file.write(str(counter + 1))
    return counter


def decrement():
    counter_file = open("counter")
    counter = int(counter_file.read())

    counter_file.close()
    counter_file = open("counter", 'w')
    counter_file.write(str(counter - 1))


def login(email, password):
    r_login_token = requests.get("https://www.poliigon.com/login", headers=headers, proxies=proxies)
    token = r_login_token.text[r_login_token.text.index("<input name=\"_token\" type=\"hidden\" value=\"") + 42:
    r_login_token.text.index("<input name=\"_token\" type=\"hidden\" value=\"") + 82]

    # Login
    payload = {"_token": token, "email": email, "password": password}
    r_login = requests.post("https://www.poliigon.com/login", headers=headers, proxies=proxies, data=payload,
                            cookies=r_login_token.cookies)
    return r_login


def create_account_and_login():
    email = rand_string() + "@sharklasers.com"

    print("email is " + email)

    f_name = rand_string()
    l_name = rand_string()
    password = rand_string()

    print("Password is " + password)

    # Get Cookie
    r = requests.get("https://www.poliigon.com/register", headers=headers, proxies=proxies)

    session_cookie = r.cookies['laravel_session']

    print("Got cookie: " + session_cookie)

    body = r.text

    # Get token
    token = body[body.index("<input name=\"_token\" type=\"hidden\" value=\"") + 42:
    body.index("<input name=\"_token\" type=\"hidden\" value=\"")+82]

    print("Got token: " + token + " " + str(len(token)))

    # Register
    payload = {"_token": token, "first_name": f_name, "last_name": l_name, "email": email,
               "email_confirmation": email, "password": password, "password_confirmation": password}

    r2 = requests.post("https://www.poliigon.com/register", headers=headers, data=payload,
                  cookies=r.cookies, proxies=proxies)

    # verify
    r3 = requests.get("https://www.poliigon.com/verify", headers=headers, proxies=proxies, cookies=r.cookies)

    if r2.text != "Error in exception handler.":
        print("Sucessful register")

        time.sleep(35)
        counter = 5

        while counter > 0:
            counter -= 1
            link = read_email(email)

            if link is None:
                time.sleep(5)
            else:
                break

        if "https" in link:
            # Verify email
            print("Verifying " + link)
            print(requests.get(link, headers=headers, proxies=proxies, cookies=r.cookies))

        # Email verified, now login
        return login(email, password)

    else:
        print(r2.text)


while True:
    rLogin = create_account_and_login()

    error = False
    while not error:
        error = download_file("https://www.poliigon.com/multiple_download/" + str(get_next_num()) + "/1K",
                              rLogin.cookies)
        if error:
            decrement()
