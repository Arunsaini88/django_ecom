from oscar.apps.shipping import repository
from oscar.apps.shipping import methods
from .methods import CustomShippingMethod

class Repository(repository.Repository):
    methods = (methods.Free(), CustomShippingMethod(),)
