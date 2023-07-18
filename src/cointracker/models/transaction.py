from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Transaction(Model):
    wallet_id = columns.Text(partition_key=True)
    network = columns.Text(partition_key=True)
    bucket_id = columns.BigInt(partition_key=True)
    block_height = columns.Text(primary_key=True)
    tx_hash = columns.Text(primary_key=True)  # transaction hash
    tx_input_n = columns.Integer()
    tx_output_n = columns.Integer()
    value = columns.Text()
    balance = columns.Text()
    sent_to = columns.Text()
    spent = columns.Boolean()
    confirmations = columns.BigInt()
    status = columns.Text()
    confirmed_at = columns.DateTime()
    double_spend = columns.Boolean()
    currency = columns.Text()
