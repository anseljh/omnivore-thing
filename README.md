# omnivore-thing

## Documentation

- [Learn About Sending Documents to Your Kindle Library](https://www.amazon.com/gp/help/customer/display.html?nodeId=G5WYD9SAF7PGXRNA)
- [Learn How to Use Your Send to Kindle Email Address](https://www.amazon.com/gp/help/customer/display.html?nodeId=G7NECT4B4ZWHQ8WV)
- [Add an Email Address to Receive Documents in Your Kindle Library](https://www.amazon.com/help/receivepersonaldocuments/ref=kinw_myk_wl_ln)
- [View Kindle documents](https://www.amazon.com/hz/mycd/digital-console/contentlist/pdocs/dateDsc/)
- [W3C ePub standard](https://www.w3.org/publishing/epub3/)
- [ebooklib](https://docs.sourcefabric.org/projects/ebooklib/en/latest/)
- [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html)
- [Flask + Celery](https://flask.palletsprojects.com/en/2.3.x/patterns/celery/)

## Setup

- On Amazon, get the email address of the Kindle device you want to set up [here](https://www.amazon.com/hz/mycd/digital-console/alldevices).
- Add it to `kindle` -> `kindle_email` in `secrets.json`.
- On Amazon, go to [your preferences for digital content](https://www.amazon.com/hz/mycd/myx#/home/settings/payment). Scroll down to Personal Document Settings. Add %%TBD%% to the "Approved Personal Document E-mail List".

## Process

- Receive webhook from Omnivore
- Parse webhook
- Retrieve article full text from Omnivore
- Generate ePub file
- Send email to Kindle Personal Documents Service email address with ePub attachment

## Architecture

- Flask app for receiving webhook
- Celery task queue
- [eBookLib](https://pypi.org/project/EbookLib/) ePub generator
- Mailgun email

## `secrets.json` Contents

Create a file called `secrets.json` and add these values:

```json
{
    "omnivore": {
        "api_key": ""
    },
    "mailgun": {
        "api_key": "",
        "api_base": "",
        "domain": ""
    },
    "amazon": {
        "kindle_email": ""
    }
}
```
