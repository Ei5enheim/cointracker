from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class User(Model):
    id = columns.UUID
    email = columns.Text(primary_key=True)
    first_name = columns.Text()
    last_name = columns.Text()
    created_at = columns.DateTime()
    updated_at = columns.DateTime()
    wallets = columns.Map(columns.Text(), columns.List(columns.Text()))
    last_crawled_at = columns.DateTime()
    bucket_id = columns.Integer()
