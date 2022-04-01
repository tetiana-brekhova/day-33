import requests
from datetime import datetime
import smtplib

MY_LAT = 50.447731
MY_LONG = 30.542721
ACCOUNT = "andretan.test@gmail.com"
PASSWORD = "q-1w-2e-3"


def is_place():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    data = response.json()["iss_position"]
    longitude = data["longitude"]
    latitude = data["latitude"]
    if MY_LONG-5 < longitude < MY_LONG+5 and MY_LAT-5 < latitude < MY_LAT+5:
        return True


def is_night():
    parameter = {"lat": MY_LAT, "long": MY_LONG, "formatted": 0}
    response = requests.get(url="https://api.sunrise-sunset.org/json?", params=parameter).json()
    sunrise = int(response["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(response["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = int(datetime.now().hour)
    if sunrise > time_now > sunset:
        return True


if is_place() and is_night():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=ACCOUNT, password=PASSWORD)
        connection.sendmail(from_addr=ACCOUNT,
                            to_addrs=ACCOUNT,
                            msg="Subject:Look up\n\n It's time!")
