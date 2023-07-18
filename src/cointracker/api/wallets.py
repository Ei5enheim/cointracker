import json
import time

import falcon
import falcon.asgi
from blockcypher.utils import is_valid_address_for_coinsymbol

from cointracker.models.network import Network
from cointracker.network.integration import NetworkIntegration
from cointracker.storage.engine import StorageEngine


class Wallets:
    # max number of transactions in a bucket.
    PAGE_SIZE = 100
    # max number of buckets.
    MAX_BUCKETS = 10

    def __init__(self, storage: StorageEngine, network_integration: NetworkIntegration):
        self.storage = storage
        self.network_integration = network_integration

    async def on_get(self, req, resp):
        try:
            entries = self.storage.get_all_wallets()
            resp.text = json.dumps(entries, indent=4, sort_keys=True, default=str)
        except Exception as e:
            print(e)
            raise e

    async def on_get_user_wallet(self, req, resp, user_id, network, address):
        self.get_wallet(req, resp, network, address)

    async def on_get_wallet(self, req, resp, network, address):
        self.get_wallet(req, resp, network, address)

    def get_wallet(self, req, resp, network, address):

        if network not in [Network.BTC.value]:
            resp.status = falcon.HTTP_400
            resp.text = "invalid network"
            return

        network = Network.BTC
        try:
            entry = self.storage.get_wallet(network, address)
            resp.text = json.dumps(dict(entry), indent=4, sort_keys=True, default=str)
        except Exception as e:
            print(e)
            raise e

    async def on_delete_user_wallet(self, req, resp, user_id, network, address):

        if network not in [Network.BTC.value]:
            resp.status = falcon.HTTP_400
            resp.text = "invalid network"
            return

        network = Network.BTC
        try:
            user_inst = self.storage.get_user(user_id)
            if user_inst is None:
                resp.status = falcon.HTTP_404
                resp.text = "Resource not found"
                return
            entry = self.storage.remove_wallet(network, address, user_inst)
            resp.text = json.dumps(dict(entry), indent=4, sort_keys=True, default=str)
        except Exception as e:
            print(e)
            raise e

    async def on_post_user_wallet(self, req, resp, user_id, network, address):

        if network not in [Network.BTC.value]:
            resp.status = falcon.HTTP_400
            resp.text = "invalid network"
            return

        network = Network.BTC
        try:
            is_valid_address_for_coinsymbol(address, network.value)
        except AssertionError as e:
            print(e)
            resp.status = falcon.HTTP_400
            resp.text = "invalid wallet address"
            return

        try:
            user_inst = self.storage.get_user(user_id)
            if user_inst is None:
                resp.status = falcon.HTTP_404
                resp.text = "Resource not found"
                return

            entry = self.storage.add_wallet(network, address, user_inst)
            resp.text = json.dumps(dict(entry), indent=4, sort_keys=True, default=str)
        except Exception as e:
            print(e)
            raise e

        # TODO make this asynchronous
        # get wallet balance details
        wallet = None
        try:
            balance_details = self.network_integration.get_balance(network, address)
            wallet = self.storage.add_wallet_details(
                network,
                address,
                str(balance_details["total_received"]),
                str(balance_details["total_sent"]),
                str(balance_details["balance"]),
                str(balance_details["unconfirmed_balance"]),
                balance_details["n_tx"],
                balance_details["final_n_tx"],
                balance_details["unconfirmed_n_tx"],
            )

        except Exception as e:
            print(e)

        max_bucket_id, min_bucket_id = self.MAX_BUCKETS - 1, 0
        has_more = True
        bucket_id = max_bucket_id
        before = None
        try:
            while bucket_id >= min_bucket_id and has_more > 0:
                details = self.network_integration.get_transactions_before(
                    network, address, before, self.PAGE_SIZE
                )
                has_more = details["hasMore"]
                txns = details.get("txrefs", [])
                n_txns = len(txns)
                if n_txns == 0:
                    break

                before = txns[-1]["block_height"]
                self.storage.add_transactions(
                    wallet, txns, max_bucket_id, bucket_id, bucket_id
                )
                bucket_id -= 1
                time.sleep(0.25)

        except Exception as e:
            print(e)
            raise e
