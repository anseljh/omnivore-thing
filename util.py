import json


def load_secrets() -> str:
    with open("secrets.json") as secrets_f:
        secrets = json.load(secrets_f)
        return secrets

def get_api_key() -> str:
    secrets = load_secrets()
    return secrets.get("api_key")
