import requests
from datetime import datetime
import smtplib
import time
import os

MY_LATITUDE = 31.215870
MY_LONGITUDE = 31.357010


def pos_of_ISS():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if (
        MY_LATITUDE - 5 <= iss_latitude <= MY_LATITUDE + 5
        and MY_LONGITUDE - 5 <= iss_longitude <= MY_LONGITUDE + 5
    ):
        return True
    else:
        return False


parameters = {
    "lat": MY_LATITUDE,
    "lng": MY_LONGITUDE,
    "formatted": 0,
    "tzid": "Africa/Cairo",
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
time_now = datetime.now()

if time_now.hour >= sunset or time_now.hour <= sunrise:
    if pos_of_ISS():
        MY_EMAIL = os.getenv("MY_EMAIL")
        MY_PASSWORD = os.getenv("MY_PASSWORD")
        EMAIL = os.getenv("EMAIL")
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=EMAIL,
                msg=f"Subject:ISS_TRACKER\n\n LOOK UP👆",
            )
            connection.close()
