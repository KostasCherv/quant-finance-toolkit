class ZeroCouponBond:
    def __init__(self, principal, maturity, interest_rate):
        self.principal = principal
        self.maturity = maturity
        self.interest_rate = interest_rate / 100

    def preset_value(self, x, n):
        return x / (1 + self.interest_rate) ** n

    def calculate_price(self):
        return self.preset_value(self.principal, self.maturity)


if __name__ == "__main__":
    bond = ZeroCouponBond(1000, 2, 4)
    print(bond.calculate_price())
