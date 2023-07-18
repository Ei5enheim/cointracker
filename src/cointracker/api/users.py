import json

import falcon

from cointracker.storage.engine import StorageEngine


class Users:
    def __init__(self, storage: StorageEngine):
        self.storage = storage

    async def on_get(self, req, resp):
        try:
            entries = self.storage.get_all_users()
            resp.body = json.dumps(entries, indent=4, sort_keys=True, default=str)
            # resp.set_header('Access-Control-Allow-Origin', '*')
        except Exception as e:
            print(e)
            raise e

    async def on_get_user(self, req, resp, user_id):
        try:
            entry = self.storage.get_user(user_id)
            resp.text = json.dumps(dict(entry), indent=4, sort_keys=True, default=str)
        except Exception as e:
            print(e)
            raise e
