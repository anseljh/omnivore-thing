from pprint import pprint

import requests

from util import get_api_key

QUERY = """{
  page {
    title
    description
    author
    url
    wordsCount
  }
}"""

QUERY2 = """{
    article {
        ... on ArticleSuccess {
            article {
                id
                title
                description
                author
                url
                wordsCount            
            }
        }
        ... on ArticleError {
            errorCodes
        }
    }
}"""

QUERY_LABELS = '''{
    labels {
        ... on LabelsSuccess {
            labels {
                id
                name
                color
                description
                createdAt
            }
        }
        ... on LabelsError {
            errorCodes
        }
    }
}
    '''

API_BASE = "https://api-prod.omnivore.app/api/graphql"
TEST_PAGE_ID = "08a9211f-e1eb-4d02-b78c-6622abdb04e5"
API_KEY = None

if __name__ == "__main__":
    API_KEY = get_api_key()
    headers = {
        # "Authorization": f"Bearer {API_KEY}",
        # "Cookie": f"auth={API_KEY};",
        "Authorization": API_KEY,
    }
    body = {
        # "query": QUERY,
        # "variables": { "id": TEST_PAGE_ID },
        # "query": QUERY_LABELS, ## works!
        "query": QUERY2,
    }
    
    response = requests.post(API_BASE, headers=headers, json=body)
    
    print(response.status_code)
    pprint(dict(response.headers))
    print()
    print(response.text)
    print()
    pprint(dict(response.request.headers))
    pprint(response.request.body)
