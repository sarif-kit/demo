import json
import os


def Total(order):
    """Return the amount owed for an order."""
    currency = order["currency"]
    lines = order["lines"]
    return sum(line["price"] * line["qty"] for line in lines) - discount(order)
