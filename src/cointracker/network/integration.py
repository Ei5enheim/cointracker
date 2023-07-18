from cointracker.models.network import Network


class NetworkIntegration:
    def get_transactions_before(
        self, network: Network, address: str, transactions_before: str, page_size: int
    ):
        raise NotImplementedError("inherit and implement as needed")

    def get_transactions_after(
        self, network: Network, address: str, transactions_after: str, page_size: int
    ):
        raise NotImplementedError("inherit and implement as needed")

    def get_balance(self, network: Network, address: str):
        raise NotImplementedError("inherit and implement as needed")
