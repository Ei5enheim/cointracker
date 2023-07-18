import base64
import json
import traceback

import falcon
import falcon.asgi

from cointracker.models.network import Network
from cointracker.network.integration import NetworkIntegration
from cointracker.storage.engine import StorageEngine


class Transactions:
    TX_HASH = "tx_hash"
    BUCKET_ID = "bucket_id"
    BLOCK_HEIGHT = "block_height"

    def __init__(self, storage: StorageEngine, network_integration: NetworkIntegration):
        self.storage = storage
        self.network_integration = network_integration

    def parse_token(self, token_str: str):
        if token_str is None:
            return (None, None, None)
        data = base64.b64decode(token_str)
        d = json.loads(data)
        return (
            d.get(self.TX_HASH, None),
            d.get(self.BUCKET_ID, None),
            d.get(self.BLOCK_HEIGHT, None),
        )

    # helper methods
    def find_indx(self, entries, tx_hash):
        if tx_hash is None:
            return None
        for i in range(0, len(entries)):
            if entries[i]["tx_hash"] == tx_hash:
                return i
        return None

    def serialize_token(self, tx_hash, bucket_id, block_height):
        d = {
            self.TX_HASH: tx_hash,
            self.BUCKET_ID: bucket_id,
            self.BLOCK_HEIGHT: block_height,
        }
        return base64.b64encode(json.dumps(d).encode())

    def get_bucket_id(self, bucket_id, wallet):
        if bucket_id is None:
            return wallet.transactions_max_bucket_id
        return bucket_id

    def get_items_to_copy(self, entries, tx_hash, limit):
        indx = self.find_indx(entries, tx_hash)
        if indx is None:
            indx = -1
        # indx is exclusive
        num_items_to_copy = min(len(entries) - (indx + 1), limit)
        items_to_copy = entries[indx + 1 : indx + num_items_to_copy + 1]
        return items_to_copy

    async def on_get_transactions(self, req, resp, network, address):
        if network not in [Network.BTC.value]:
            resp.status = falcon.HTTP_400
            resp.text = "invalid network"
            return

        network = Network.BTC
        wallet = self.storage.get_wallet(network, address)
        limit = int(req.get_param("limit", default=100))
        token_str = req.get_param("token", default=None)

        out = []
        tx_hash, bucket_id, block_height = self.parse_token(token_str)
        bucket_id = self.get_bucket_id(bucket_id, wallet)
        print("input is: ", network, address, limit, bucket_id, tx_hash, block_height)
        while limit > 0 and bucket_id >= wallet.transactions_min_bucket_id:
            try:
                entries = self.storage.get_transactions(network, address, bucket_id)
            except Exception as e:
                traceback.print_exc()
                raise e

            items_to_copy = self.get_items_to_copy(entries, tx_hash, limit)
            out.extend(items_to_copy)
            # reset tx_hash
            limit -= len(items_to_copy)
            # reset tx_hash
            tx_hash = out[len(out) - 1]["tx_hash"]
            block_height = out[len(out) - 1]["block_height"]
            if limit > 0:
                bucket_id = bucket_id - 1

        # get entries from network starting with 
        # block height less than that of the last item.
        # because there 
        has_more = True
        while limit > 0 and has_more:
            try:
                details = self.network_integration.get_transactions_before(
                    network, address, block_height, limit
                )
            except Exception as e:
                traceback.print_exc()
                raise e

            has_more = details["hasMore"]
            txns = details.get("txrefs", [])
            # sort the entries in reverse order
            sorted(
                txns, key=lambda x: str(x["block_height"]) + x["tx_hash"], reverse=True
            )
            items_to_copy = self.get_items_to_copy(txns, tx_hash, limit)
            out.extend(items_to_copy)
            # reset tx_hash
            limit -= len(items_to_copy)
            tx_hash = out[len(out) - 1]["tx_hash"]
            block_height = out[len(out) - 1]["block_height"]

        token_str = self.serialize_token(
            out[len(out) - 1]["tx_hash"], bucket_id, out[len(out) - 1]["block_height"]
        )
        resp.text = json.dumps(out, indent=4, sort_keys=True, default=str)
        resp.set_header("X-Token", token_str)
