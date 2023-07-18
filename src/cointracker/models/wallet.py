from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Wallet(Model):
    address = columns.Text(partition_key=True)
    network = columns.Text(partition_key=True)
    total_received = columns.Text()
    total_sent = columns.Text()
    balance = columns.Text()
    unconfirmed_balance = columns.BigInt()
    number_transactions = columns.BigInt()
    confirmed_transactions = columns.BigInt()
    unconfirmed_transactions = columns.BigInt()
    last_updated_at = columns.DateTime()
    currency = columns.Text()
    transactions_max_bucket_id = columns.BigInt()
    transactions_min_bucket_id = columns.BigInt()
    number_transactions_stored = columns.BigInt()
