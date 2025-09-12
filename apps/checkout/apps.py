import oscar.apps.checkout.apps as apps


class CheckoutConfig(apps.CheckoutConfig):
    name = 'apps.checkout'


# from oscar.apps.checkout import app
# from .views import PaymentDetailsView

# class CheckoutApplication(app.CheckoutApplication):
#     payment_details_view = PaymentDetailsView


# application = CheckoutApplication()