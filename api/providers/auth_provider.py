import json
import os

_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data")
)

ROOT_PATH = _ROOT + os.sep

def _load_users():
    with open(ROOT_PATH + "user.json", "r") as f:
        return json.load(f)

def get_user(api_key):
    users = _load_users()
    for x in users:
        if x["api_key"] == api_key:
            return x
    return None

def has_access(user, paths, method):
    access = user["endpoint_access"]
    # The resource name is always the first segment (e.g. ["warehouses", "3"]).
    resource = paths[0]
    if resource not in access:
        return False
    perms = access[resource]
    return perms.get(method, False)