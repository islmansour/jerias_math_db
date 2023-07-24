from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from jerias_production.models import Payment, Person, Purchase, Account


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


@csrf_exempt
def create_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            purchaseRec = data.get('purchase')

            # Check if the associated Purchase exists

            purchase = Purchase.objects.get(id=purchaseRec.get('id'))

            # Create a new Payment object
            payment = Payment(purchase=purchase)

            # Update the Payment object with the fields from the JSON data
            createdBy_data = data.get('createdBy')
            if createdBy_data:
                createdBy_id = createdBy_data.get('id')
                if createdBy_id:
                    try:
                        createdBy = Person.objects.get(id=createdBy_id)
                        payment.createdBy = createdBy
                    except Person.DoesNotExist:
                        return JsonResponse({'success': False, 'message': 'createdBy not found'}, status=404)

            lastUpdatedBy_data = data.get('lastUpdatedBy')
            if lastUpdatedBy_data:
                lastUpdatedBy_id = lastUpdatedBy_data.get('id')
                if lastUpdatedBy_id:
                    try:
                        lastUpdatedBy = Person.objects.get(id=lastUpdatedBy_id)
                        payment.lastUpdatedBy = lastUpdatedBy
                    except Person.DoesNotExist:
                        return JsonResponse({'success': False, 'message': 'Last updated by not found'}, status=404)

            account_data = data.get('account')
            if account_data:
                account_id = account_data.get('id')
                if account_id:
                    try:
                        account = Account.objects.get(id=account_id)
                        payment.account = account
                    except Account.DoesNotExist:
                        return JsonResponse({'success': False, 'message': 'Account not found'}, status=404)

            payment.amount = data.get('amount')
            payment.paymentType = data.get('paymentType')
            payment.chequeNumber = data.get('chequeNumber')
            payment.chequeBank = data.get('chequeBank')
            payment.chequeDate = timezone.datetime.strptime(data.get(
                'chequeDate'), '%Y-%m-%dT%H:%M:%S.%fZ') if data.get('chequeDate') else None
            payment.notes = data.get('notes')

            # Save the Payment object
            payment.save()

            response_data = {
                'success': True,
                'message': 'Payment created successfully'
            }
            return JsonResponse(response_data, status=201)
        except Exception as e:
            response_data = {
                'success': False,
                'message': str(e)
            }
            print(response_data)
            return JsonResponse(response_data, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
