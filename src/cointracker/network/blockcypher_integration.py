import blockcypher

from cointracker.models.network import Network
from cointracker.network.integration import NetworkIntegration


class BlockCypher(NetworkIntegration):
    def __init__(self):
        pass

    def get_transactions_before(
        self, network: Network, address: str, transactions_before: str, page_size: int
    ):
        # Get address details
        address_details = blockcypher.get_address_details(
            address, network.value, txn_limit=page_size, before_bh=transactions_before
        )

        return address_details

    def get_transactions_after(
        self, network: Network, address: str, transactions_after: str, page_size: int
    ):
        # Get address details
        address_details = blockcypher.get_address_details(
            address, network.value, txn_limit=page_size, after_bh=transactions_after
        )
        return address_details

    def get_balance(self, network: Network, address: str):
        balance_details = blockcypher.get_address_overview(address, network.value)
        return balance_details
