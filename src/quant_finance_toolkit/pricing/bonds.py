"""Bond pricing models for zero-coupon and coupon bonds."""

from math import exp

from .present_value import (
    present_continuous_value,
    present_discrete_value,
)


class ZeroCouponBond:
    """Zero-coupon bond pricing model.

    A zero-coupon bond pays no periodic interest and is sold at a discount,
    paying the face value at maturity.

    Parameters
    ----------
    principal : float
        Face value of the bond
    maturity : int
        Years to maturity
    interest_rate : float
        Annual interest rate as percentage (e.g., 4 for 4%)

    Examples
    --------
    >>> bond = ZeroCouponBond(1000, 2, 4)
    >>> bond.calculate_price()
    924.5562130177715
    """

    def __init__(self, principal: float, maturity: int, interest_rate: float) -> None:
        self.principal = principal
        self.maturity = maturity
        self.interest_rate = interest_rate / 100

    def calculate_price(self) -> float:
        """Calculate the present value (price) of the zero-coupon bond.

        Returns
        -------
        float
            Bond price
        """
        return present_discrete_value(self.principal, self.interest_rate, self.maturity)


class CouponBond:
    """Coupon bond pricing model.

    A coupon bond pays periodic interest payments (coupons) and returns
    the principal at maturity.

    Parameters
    ----------
    principal : float
        Face value of the bond
    rate : float
        Annual coupon rate as percentage (e.g., 10 for 10%)
    maturity : int
        Years to maturity
    interest_rate : float
        Market interest rate (discount rate) as percentage (e.g., 4 for 4%)

    Examples
    --------
    >>> bond = CouponBond(1000, 10, 3, 4)
    >>> price = bond.calculate_price()
    >>> price > 1000  # Premium bond (coupon rate > market rate)
    True
    """

    def __init__(
        self, principal: float, rate: float, maturity: int, interest_rate: float
    ) -> None:
        self.principal = principal
        self.rate = rate / 100
        self.maturity = maturity
        self.interest_rate = interest_rate / 100

    def calculate_price(self) -> float:
        """Calculate bond price using discrete compounding.

        Returns
        -------
        float
            Bond price
        """
        price = 0.0
        # Discount coupon payments
        for t in range(1, self.maturity + 1):
            price += present_discrete_value(self.principal * self.rate, self.interest_rate, t)

        # Add discounted principal payment
        return price + present_discrete_value(self.principal, self.interest_rate, self.maturity)

    def calculate_continuous_price(self) -> float:
        """Calculate bond price using continuous compounding.

        Returns
        -------
        float
            Bond price with continuous compounding
        """
        price = 0.0
        # Discount coupon payments
        for t in range(1, self.maturity + 1):
            price += present_continuous_value(self.principal * self.rate, self.interest_rate, t)

        # Add discounted principal payment
        return price + present_continuous_value(
            self.principal, self.interest_rate, self.maturity
        )
