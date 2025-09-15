from django import shortcuts
from oscar.apps.basket.views import BasketAddView as CoreBasketAddView
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic import View
from oscar.core.loading import get_class, get_model
from oscar.core.utils import is_ajax

Applicator = get_class("offer.applicator", "Applicator")
AddToBasketForm = get_class("basket.forms", "AddToBasketForm")

class BasketAddView(CoreBasketAddView,View):
    """
    Handles the add-to-basket requests via AJAX.
    """

    product_model = get_model("catalogue", "product")
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        # Get product by product_id passed via AJAX
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity', 1)

        try:
            product = self.product_model.objects.get(pk=product_id)
        except self.product_model.DoesNotExist:
            return JsonResponse({'success': False, 'message': _("Product does not exist.")}, status=404)

        # Handle AJAX request
        if is_ajax(request):
            return self.handle_ajax_request(request, product, quantity)

        # return JsonResponse({'success': False, 'message': _("Invalid request.")}, status=400)
        # Handle non-AJAX request
        return super().post(request, *args, **kwargs) # Call the parent post method

    def handle_ajax_request(self, request, product, quantity):
        """
        Handles the basket addition via AJAX request.
        """
        # Add the product to the basket with the specified quantity
        try:
            quantity = int(quantity)
            request.basket.add_product(product, quantity)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

        # Prepare the response
        response_data = {
            'success': True,
            'message': _("Product added to basket."),
            'product_id': product.pk,
            'quantity': quantity,
            'product': {
                'name': product.get_title(),  # Assuming product has get_title() method for display
            }
        }

        # Send success response back to AJAX
        return JsonResponse(response_data)
