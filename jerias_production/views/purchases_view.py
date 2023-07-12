from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from jerias_production.models import Payment, Purchase


@csrf_exempt
def purchases_by_student(request):
    student_id = int(request.GET.get('student_id'))  # Convert to integer
    try:
        purchases = Purchase.objects.filter(student_id=student_id)
        data = []

        for purchase in purchases:
            print('--------------------- foiund ------------------')
            payments = Payment.objects.filter(purchase=purchase)
            payment_data = []

            for payment in payments:
                payment_data.append(payment.to_json())

            purchase_data = {
                'id': purchase.id,
                'createdBy': purchase.createdBy.to_json() if purchase.createdBy else None,
                'created': purchase.created.isoformat() if purchase.created else None,
                'lastUpdated': purchase.lastUpdated.isoformat() if purchase.lastUpdated else None,
                'lastUpdatedBy': purchase.lastUpdatedBy.to_json() if purchase.lastUpdatedBy else None,
                'status': purchase.status,
                'autoGenerate': purchase.autoGenerate,
                'student': purchase.student.to_json() if purchase.student else None,
                'amount': purchase.amount,
                'maxAttendances': purchase.maxAttendances,
                'account': purchase.account.to_json() if purchase.account else None,
                'payments': payment_data,
            }

            data.append(purchase_data)

        return JsonResponse(data, status=201, safe=False)

    except Exception as e:
        response_data = {
            'response_status': 'error',
            'message': str(e)
        }
        return JsonResponse(response_data, status=400, safe=False)
