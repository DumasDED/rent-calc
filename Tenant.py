from decimal import Decimal


class Tenant:
    def __init__(self, name, rent, utilities=[]):
        self.name = name
        self.rent = Decimal(rent)
        self.utilities = {}
        for u in utilities:
            self.utilities[u] = Decimal(0)
        self.owes = Decimal(0)
        self.adjustment = Decimal(0)

    def paid(self):
        return sum(self.utilities.values())

    def remaining(self):
        return self.owes - self.paid()

    def total(self):
        return self.rent + self.remaining()