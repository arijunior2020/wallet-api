class WalletRepository:
    def __init__(self):
        self.wallets = {}
        self.wallet_id_counter = 1

    def create_wallet(self, name):
        wallet_id = self.wallet_id_counter
        self.wallets[wallet_id] = {"id": wallet_id, "name": name, "balance": 0.0}
        self.wallet_id_counter += 1
        return self.wallets[wallet_id]

    def get_wallet(self, wallet_id):
        return self.wallets.get(wallet_id)

    def update_wallet(self, wallet_id, name):
        wallet = self.wallets.get(wallet_id)
        if wallet:
            wallet["name"] = name
        return wallet

    def delete_wallet(self, wallet_id):
        return self.wallets.pop(wallet_id, None)

    def deposit(self, wallet_id, amount):
        wallet = self.wallets.get(wallet_id)
        if wallet:
            wallet["balance"] += amount
        return wallet

    def withdraw(self, wallet_id, amount):
        wallet = self.wallets.get(wallet_id)
        if wallet and wallet["balance"] >= amount:
            wallet["balance"] -= amount
            return wallet
        return None

    def transfer(self, from_wallet_id, to_wallet_id, amount):
        from_wallet = self.wallets.get(from_wallet_id)
        to_wallet = self.wallets.get(to_wallet_id)
        if from_wallet and to_wallet and from_wallet["balance"] >= amount:
            from_wallet["balance"] -= amount
            to_wallet["balance"] += amount
            return {"from_wallet": from_wallet, "to_wallet": to_wallet}
        return None
