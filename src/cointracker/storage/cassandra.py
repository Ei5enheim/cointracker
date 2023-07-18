from datetime import datetime
from typing import List

from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.query import BatchQuery

from cointracker.models.network import Network
from cointracker.models.transaction import Transaction
from cointracker.models.user import User
from cointracker.models.wallet import Wallet
from cointracker.storage.engine import StorageEngine


class CassandraStorageEngine(StorageEngine):
    CLUSTER = "cluster"

    def __init__(self, ips: List[str], key_space: str):
        try:
            self.cluster = Cluster(ips)
            self.key_space = key_space
            self.session = self.cluster.connect(key_space)
            connection.register_connection(self.CLUSTER, session=self.session)
            connection.set_session(self.session)
            sync_table(Wallet)
            sync_table(User)
            sync_table(Transaction)
        except Exception as e:
            print("Failed to setup Cassandra: ", e.errors)
            raise e

    def get_all_users(self):
        q = User.objects
        entries = q.using(keyspace=self.key_space, connection=self.CLUSTER).all()
        result = []
        for e in entries:
            result.append(dict(e))
        return result

    def get_user(self, id: str):
        q = User.filter(email_id=id)
        if q.count() < 1:
            return None
        return q[0]

    def get_all_wallets(self):
        q = Wallet.objects
        entries = q.using(keyspace=self.key_space, connection=self.CLUSTER).all()
        result = []
        for e in entries:
            result.append(dict(e))
        return result

    def add_wallet(self, network: Network, address: str, user: User):
        wallets = user.wallets
        network_wallets = wallets.get(network.value, [])
        if address not in network_wallets:
            network_wallets.append(address)
        wallets[network.value] = network_wallets
        user.wallets = wallets
        user.updated_at = datetime.utcnow()
        user.update()
        return user

    def remove_wallet(self, network: Network, address: str, user: User):
        wallets = user.wallets
        print(wallets)
        network_wallets = wallets.get(network.value, [])
        if address in network_wallets:
            network_wallets.remove(address)
            wallets[network.value] = network_wallets
            user.wallets = wallets
            user.updated_at = datetime.utcnow()
            user.update()
        return user

    def get_wallet(self, network: Network, address: str):
        q = Wallet.filter(address=address, network=network.value)
        if q.count() < 1:
            return None
        return q[0]

    def update_wallet_details(
        self,
        network: Network,
        address: str,
        total_received: str,
        total_sent: str,
        balance: str,
        unconfirmed_balance: int,
        number_transactions: int,
        confirmed_transactions: int,
        unconfirmed_transactions: int,
    ):
        timestamp = datetime.utcnow()
        wallet = self.get_wallet(network, address)
        wallet.total_received = total_received
        wallet.total_sent = total_sent
        wallet.balance = balance
        wallet.unconfirmed_balance = unconfirmed_balance
        wallet.number_transactions = number_transactions
        wallet.confirmed_transactions = confirmed_transactions
        wallet.unconfirmed_transactions = unconfirmed_transactions
        wallet.last_updated_at = timestamp
        wallet.update()
        return wallet

    def add_wallet_details(
        self,
        network: Network,
        address: str,
        total_received: str,
        total_sent: str,
        balance: str,
        unconfirmed_balance: str,
        number_transactions: int,
        confirmed_transactions: int,
        unconfirmed_transactions: int,
    ):
        timestamp = datetime.utcnow()
        wallet = Wallet.create(
            address=address,
            network=network.value,
            total_received=total_received,
            total_sent=total_sent,
            balance=balance,
            unconfirmed_balance=unconfirmed_balance,
            number_transactions=number_transactions,
            confirmed_transactions=confirmed_transactions,
            unconfirmed_transactions=unconfirmed_transactions,
            number_transactions_stored=0,
            last_updated_at=timestamp,
        )
        return wallet

    def add_transactions(
        self, wallet: Wallet, txns, max_bucket_id, min_bucket_id, bucket_id
    ):
        b = BatchQuery()
        for tx in txns:
            Transaction.batch(b).create(
                wallet_id=wallet.address,
                network=wallet.network,
                bucket_id=bucket_id,
                block_height=str(tx["block_height"]),
                tx_hash=tx["tx_hash"],
                tx_input_n=tx["tx_input_n"],
                tx_output_n=tx["tx_output_n"],
                value=str(tx["value"]),
                balance=str(tx["ref_balance"]),
                spent=tx.get("spent", True),
                confirmations=tx["confirmations"],
                confirmed_at=tx["confirmed"],
            )
        wallet.transactions_max_bucket_id = max_bucket_id
        wallet.transactions_min_bucket_id = min_bucket_id
        wallet.number_transactions_stored += len(txns)
        wallet.batch(b).save()
        b.execute()

    def get_transactions(self, network: Network, address: str, bucket_id: int):
        entries = Transaction.filter(
            wallet_id=address, network=network.value, bucket_id=bucket_id
        )
        if entries.count() < 1:
            return []
        result = []
        for e in entries:
            result.append(dict(e))
        result.reverse()
        return result
