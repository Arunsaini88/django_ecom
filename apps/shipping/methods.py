from oscar.apps.shipping import methods
from oscar.core import prices
from decimal import Decimal as D

class CustomShippingMethod(methods.FixedPrice):
    code = 'custom_shipping'
    name = 'Express Shipping'
    charge_excl_tax = D("10.00")
    charge_incl_tax = D("10.01")