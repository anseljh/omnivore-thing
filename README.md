# omnivore-thing

## Documentation

- [Learn About Sending Documents to Your Kindle Library](https://www.amazon.com/gp/help/customer/display.html?nodeId=G5WYD9SAF7PGXRNA)
- [Learn How to Use Your Send to Kindle Email Address](https://www.amazon.com/gp/help/customer/display.html?nodeId=G7NECT4B4ZWHQ8WV)
- [W3C ePub standard](https://www.w3.org/publishing/epub3/)
- [ebooklib](https://docs.sourcefabric.org/projects/ebooklib/en/latest/)
- [Flask + Celery](https://flask.palletsprojects.com/en/2.3.x/patterns/celery/)
- [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html)
- [View Kindle documents](https://www.amazon.com/hz/mycd/digital-console/contentlist/pdocs/dateDsc/)

## Setup

- Get the email address of the Kindle device you want to set up [here](https://www.amazon.com/hz/mycd/digital-console/alldevices).
- Add it to `kindle` -> `kindle_email` in `secrets.json`.

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
