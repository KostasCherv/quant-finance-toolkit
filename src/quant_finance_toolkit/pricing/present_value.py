"""Time value of money calculations for discrete and continuous compounding."""

from math import exp


def future_discrete_value(x: float, r: float, n: int) -> float:
    """Calculate future value with discrete compounding.

    Parameters
    ----------
    x : float
        Present value or principal amount
    r : float
        Interest rate (as decimal, e.g., 0.05 for 5%)
    n : int
        Number of periods

    Returns
    -------
    float
        Future value after n periods

    Examples
    --------
    >>> future_discrete_value(100, 0.05, 5)
    127.62815625000003
    """
    return x * (1 + r) ** n


def present_discrete_value(x: float, r: float, n: int) -> float:
    """Calculate present value with discrete compounding.

    Parameters
    ----------
    x : float
        Future value
    r : float
        Interest rate (as decimal, e.g., 0.05 for 5%)
    n : int
        Number of periods

    Returns
    -------
    float
        Present value

    Examples
    --------
    >>> present_discrete_value(127.63, 0.05, 5)
    100.0
    """
    return x / (1 + r) ** n


def future_continuous_value(x: float, r: float, t: float) -> float:
    """Calculate future value with continuous compounding.

    Parameters
    ----------
    x : float
        Present value or principal amount
    r : float
        Interest rate (as decimal, e.g., 0.05 for 5%)
    t : float
        Time in years

    Returns
    -------
    float
        Future value after t years

    Examples
    --------
    >>> future_continuous_value(100, 0.05, 5)
    128.40254166877415
    """
    return x * exp(r * t)


def present_continuous_value(x: float, r: float, t: float) -> float:
    """Calculate present value with continuous compounding.

    Parameters
    ----------
    x : float
        Future value
    r : float
        Interest rate (as decimal, e.g., 0.05 for 5%)
    t : float
        Time in years

    Returns
    -------
    float
        Present value

    Examples
    --------
    >>> present_continuous_value(128.40, 0.05, 5)
    100.0
    """
    return x * exp(-r * t)
