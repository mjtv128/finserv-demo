class InMemoryAccountRepository:
    def __init__(self, accounts):
        self._accounts = {a.id: a for a in accounts}

    def get(self, account_id):
        return self._accounts[account_id]