from math import exp


class CouponBond:
    def __init__(self, principal, rate, maturity, interest_rate):
        self.principal = principal
        self.rate = rate / 100
        self.maturity = maturity
        self.interest_rate = interest_rate / 100

    def preset_value(self, x, n):
        return x / (1 + self.interest_rate) ** n

    def calculate_price(self):
        price = 0
        # discount coupon payments
        for t in range(1, self.maturity + 1):
            price = price + self.preset_value(self.principal * self.rate, t)

        # total payment
        return price + self.preset_value(self.principal, self.maturity)

    def present_continuous_value(self, x, n):
        return x * exp(-self.interest_rate * n)

    def calculate_continuous_price(self):
        price = 0
        # discount coupon payments
        for t in range(1, self.maturity + 1):
            price = price + self.present_continuous_value(self.principal * self.rate, t)

        # total payment
        return price + self.present_continuous_value(self.principal, self.maturity)


if __name__ == "__main__":
    bond = CouponBond(1000, 10, 3, 4)
    print(f"The price of the coupon bond is {bond.calculate_price()}")
    print(
        f"The continuous price of the coupon bond is {bond.calculate_continuous_price()}"
    )
