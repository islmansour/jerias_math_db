from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from jerias_production.models import Payment, Purchase


def get_purchase_payments(request, purchase_id):
    try:
        # Retrieve the purchase object based on the purchase_id
        purchase = get_object_or_404(Purchase, pk=purchase_id)

        # Retrieve all payments associated with the purchase
        payments = Payment.objects.filter(purchase=purchase)

        # Convert payments to JSON format
        payments_json = [payment.to_json() for payment in payments]

        # Return the JSON response
        return JsonResponse(payments_json, safe=False)

    except Purchase.DoesNotExist:
        # Handle the case where the purchase does not exist
        return JsonResponse({"error": "Purchase not found"}, status=404)

    except Exception as e:
        # Handle any other exceptions that may occur
        return JsonResponse({"error": str(e)}, status=500)
