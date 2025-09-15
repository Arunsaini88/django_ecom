from django.conf import settings
from oscar.apps.payment.exceptions import UnableToTakePayment, InvalidGatewayRequestError

import razorpay
from razorpay.errors import BadRequestError, ServerError, GatewayError
from django.conf import settings


class Facade(object):
    def __init__(self):
        self.client = razorpay.Client(auth=(settings.RAZORPAY_PUBLISHABLE_KEY, settings.RAZORPAY_API_SECRET))

    @staticmethod
    def get_friendly_decline_message(error):
        return 'The transaction was declined by your bank - please check your bankcard details and try again'

    @staticmethod
    def get_friendly_error_message(error):
        return 'An error occurred when communicating with the payment gateway.'

    def charge(self,
        order_number,
        total,
        card,
        currency=settings.OSCAR_DEFAULT_CURRENCY,
        description=None,
        metadata=None,
        **kwargs):
        try:
            amount = int(total.incl_tax * 100)
            return self.client.payment.capture(card, amount)
        except (BadRequestError, GatewayError) as e:
            raise UnableToTakePayment(self.get_friendly_decline_message(e))
        except ServerError as e:
            raise InvalidGatewayRequestError(self.get_friendly_error_message(e))
        except Exception as e:
            raise InvalidGatewayRequestError(self.get_friendly_error_message(e))