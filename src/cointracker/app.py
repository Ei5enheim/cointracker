import falcon
import falcon.asgi

from cointracker.api.transactions import Transactions
from cointracker.api.users import Users
from cointracker.api.wallets import Wallets
from cointracker.network.blockcypher_integration import BlockCypher
from cointracker.storage.cassandra import CassandraStorageEngine


# falcon.asgi.App instances are callable ASGI apps...
# in larger applications the app is created in a separate file
app = falcon.asgi.App()

storage = CassandraStorageEngine(["127.0.0.1"], "cointracker")
users_server = Users(storage)
blockcypher = BlockCypher()
wallets_server = Wallets(storage, blockcypher)
txns_server = Transactions(storage, blockcypher)

# user updates
app.add_route("/v1/users/{user_id}", users_server, suffix="user")
app.add_route("/v1/users", users_server)

# wallet updates
app.add_route(
    "/v1/users/{user_id}/wallets/{network}/{address}",
    wallets_server,
    suffix="user_wallet",
)
app.add_route("/v1/wallets/{network}/{address}", wallets_server, suffix="wallet")
app.add_route("/v1/wallets", wallets_server)
app.add_route(
    "/v1/wallets/{network}/{address}/transactions", txns_server, suffix="transactions"
)
