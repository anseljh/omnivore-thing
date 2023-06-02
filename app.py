import json
from pprint import pprint

from flask import Flask, request
from ebooklib import epub
import lorem
import requests

from util import get_api_key, load_secrets

app = Flask(__name__)
secrets = load_secrets()

DEFAULT_TO_ADDRESS = secrets["amazon"]["kindle_email"]


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.post("/omnivore-webhook")
def omnivore_webhook():
    with open("content.json", "wb") as f:
        f.write(request.data)
    # with open("headers.json", "wb") as f:
    #     json.dump(dict(request.headers), f)
    pprint(dict(request.headers))
    print()
    pprint(json.loads(request.data))
    print()
    return {
        # "foo": "bar",
        # "headers": request.headers,
        # "data": request.data,
        "status": "cool",
    }


def generate_epub(
    identifier: str,
    title: str,
    author: str = None,
    content: str = None,
    language: str = "en",
    url: str = None,
):
    book = epub.EpubBook()

    # set metadata
    book.set_identifier(identifier)
    book.set_title(title)
    assert len(language) == 2
    book.set_language(language)
    if author is not None:
        book.add_author(author)

    # create chapter
    c1 = epub.EpubHtml(title=title, file_name="chap_01.xhtml", lang="hr")
    # TODO: Actual content
    c1.content = (
        f"<h1>{title}</h1>"
        f"<p>{author}</p>"
        '<p>via Omnivore. <a href="{url}">Original article</a>.</p>'
        f"<p>{lorem.paragraph()}</p>"
        f"<p>{lorem.paragraph()}</p>"
        f"<p>{lorem.paragraph()}</p>"
        f"<p>{lorem.paragraph()}</p>"
    )

    # add chapter
    book.add_item(c1)

    # define Table Of Contents
    book.toc = (
        epub.Link("chap_01.xhtml", title, "article"),  # "Introduction", "intro"),
        # (epub.Section("Article"), (c1,)),
    )

    # add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # define CSS style
    style = "BODY {color: white;}"
    nav_css = epub.EpubItem(
        uid="style_nav",
        file_name="style/nav.css",
        media_type="text/css",
        content=style,
    )

    # add CSS file
    book.add_item(nav_css)

    # basic spine
    book.spine = ["nav", c1]

    # write to the file
    output_fn = f"output/{identifier}.epub"
    epub.write_epub(output_fn, book, {})
    return output_fn


def omnivore_to_epub(om_data):
    page = om_data.get("page")
    assert page is not None

    title = page.get("title")
    assert title is not None

    author = page.get("author")
    url = page.get("url")
    description = page.get("description")
    item_type = page.get("type")
    page_type = page.get("pageType")
    published_at = page.get("publishedAt")
    page_id = page.get("id")
    ebook_id = f"omnivore-{page_id}"
    html = page.get("originalHtml")

    # TODO: Either get plain text from Omnivore, or remove the HTMl tags.

    language_full = page.get("language")
    # TODO: convert to ISO 2-character language code

    if page_type == "ARTICLE":
        pass
    else:
        print("Not an article!")
        return False

    ebook_fn = generate_epub(ebook_id, title, author, url=url)
    print(f"Wrote {ebook_fn}!")
    return ebook_fn


def email_ebook(title: str, ebook_fn: str, to_address: str = DEFAULT_TO_ADDRESS):
    mg_domain = secrets["mailgun"]["domain"]
    mg_key = secrets["mailgun"]["api_key"]
    response = requests.post(
        f"https://api.mailgun.net/v3/{mg_domain}/messages",
        auth=("api", mg_key),
        data={
            "from": f"Omnivore to Kindle <mailgun@{mg_domain}>",
            "to": [to_address],
            "subject": title,
            "text": "Not empty",
            # "html": html,
        },
        files=[
            (
                "attachment",
                (ebook_fn, open(ebook_fn, "rb").read()),
            )
        ],
    )
    print(f"Email POSTed. Status: {response.status_code}")
    if response.status_code not in (200, 201):
        pprint(response.json())


def load_from_file(fn="content.json"):
    with open(fn) as fp:
        content = json.load(fp)
        return content

def everything():
    content = load_from_file()
    title = content["page"]["title"]
    ebook_fn = omnivore_to_epub(content)
    email_ebook(title, ebook_fn)
