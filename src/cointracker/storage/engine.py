from cointracker.models.network import Network
from cointracker.models.user import User


class StorageEngine:
    def get_all_users(self):
        raise NotImplementedError("inherit and implement as needed")

    def get_user(self, id: str):
        raise NotImplementedError("inherit and implement as needed")

    def get_all_wallets(self):
        raise NotImplementedError("inherit and implement as needed")

    def add_wallet(self, network: Network, address: str, user: User):
        raise NotImplementedError("inherit and implement as needed")

    def update_wallet_details(
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
        raise NotImplementedError("inherit and implement as needed")

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
        raise NotImplementedError("inherit and implement as needed")

    def remove_wallet(self, network: Network, address: str, user: User):
        raise NotImplementedError("inherit and implement as needed")

    def get_wallet(self, network: Network, address: str):
        raise NotImplementedError("inherit and implement as needed")
