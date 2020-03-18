#!/usr/bin/env python3

import urllib.request
import smtplib
import json
import configparser
import logging
import os.path

config = configparser.ConfigParser()
config.read_file(open("kimsufi-alerts.ini"))

logging.basicConfig(
    filename="kimsufi-alerts.log",
    level=logging.DEBUG,
    format="%(asctime)s:%(message)s",
)


def model_available(model: str, country: str) -> bool:
    """Return a boolean

    Pulls availability info from ovh api for a particular model.
    """
    url = (
        "https://api.ovh.com/1.0/dedicated/server/"
        + f"availabilities?country={country}&hardware={model}"
    )
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))

    for datacenter in data[0]["datacenters"]:
        if datacenter["availability"] != "unavailable":
            return True

    return False


def send_email(results: str):
    EMAIL_USER = config["EMAIL"]["EMAIL_USER"]
    EMAIL_PASS = config["EMAIL"]["EMAIL_PASS"]
    EMAIL_DEST = config["EMAIL"]["EMAIL_DEST"]

    msg = "\r\n".join(
        [
            f"From: {EMAIL_USER}",
            f"To: {EMAIL_DEST}",
            f"Subject: Kimsufi Update",
            "",
            json.dumps(results, indent=2),
        ]
    )

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, EMAIL_DEST, msg)
        server.close()
    except Exception as e:
        logging.error(f"Email Error: {e}")


# save current state, if current state !== previous state, send email


def main():
    results_file = "/tmp/kimsufi-alerts.json"
    if os.path.isfile(results_file):
        previous_results = json.load(open(results_file))
    else:
        previous_results = []

    results = []

    for key, value in config["MODELS"].items():
        (model, country) = value.split(",")
        available = model_available(model, country)
        results.append(
            dict(alias=key, model=model, country=country, available=available)
        )

    if results != previous_results:
        send_email(results)
        json.dump(results, open(results_file, "w+"))

    logging.debug(json.dumps(results))


if __name__ == "__main__":
    main()
