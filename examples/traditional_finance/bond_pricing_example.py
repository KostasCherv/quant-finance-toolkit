"""Example: Bond pricing with zero-coupon and coupon bonds."""

from quant_finance_toolkit import CouponBond, ZeroCouponBond

# Zero-coupon bond example
print("=" * 50)
print("Zero-Coupon Bond Pricing")
print("=" * 50)
zero_bond = ZeroCouponBond(principal=1000, maturity=2, interest_rate=4)
price = zero_bond.calculate_price()
print(f"Principal: $1000")
print(f"Maturity: 2 years")
print(f"Interest Rate: 4%")
print(f"Bond Price: ${price:.2f}")
print()

# Coupon bond example
print("=" * 50)
print("Coupon Bond Pricing")
print("=" * 50)
coupon_bond = CouponBond(principal=1000, rate=10, maturity=3, interest_rate=4)
discrete_price = coupon_bond.calculate_price()
continuous_price = coupon_bond.calculate_continuous_price()
print(f"Principal: $1000")
print(f"Coupon Rate: 10%")
print(f"Maturity: 3 years")
print(f"Market Interest Rate: 4%")
print(f"Bond Price (Discrete): ${discrete_price:.2f}")
print(f"Bond Price (Continuous): ${continuous_price:.2f}")
