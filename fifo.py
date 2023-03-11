class Buyer:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


class Seller:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


class FirstInFirstOut:
    def __init__(self, buyers, sellers, default_seller):
        self.buyers = buyers
        self.sellers = sellers
        self.default_seller = default_seller
        self.transactions = []

    def run(self):
        while self.buyers and self.sellers:
            buyer = min(self.buyers, key=lambda x: x.amount)
            seller = min(self.sellers, key=lambda x: x.amount)
            if buyer.amount >= seller.amount:
                self.transactions.append((buyer.name, seller.name, seller.amount))
                buyer.amount -= seller.amount
                self.sellers.remove(seller)
            else:
                self.transactions.append((buyer.name, seller.name, buyer.amount))
                seller.amount -= buyer.amount
                self.buyers.remove(buyer)
        for buyer in self.buyers:
            self.transactions.append((buyer.name, self.default_seller, buyer.amount))
        return self.transactions


buyers = [Buyer("Buyer A", 100), Buyer("Buyer B", 200), Buyer("Buyer C", 150)]
sellers = [Seller("Seller X", 150), Seller("Seller Y", 100), Seller("Seller Z", 200)]
default_seller = "Default Seller"
system = FirstInFirstOut(buyers, sellers, default_seller)
transactions = system.run()
for transaction in transactions:
    print(f"{transaction[0]} bought from {transaction[1]} for {transaction[2]}")
