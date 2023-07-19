from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from jerias_production.models import Payment, Person, Purchase, PurchaseAttendance
from django.utils import timezone

import json


@csrf_exempt
def purchases_by_student(request):
    student_id = int(request.GET.get('student_id'))  # Convert to integer
    try:
        purchases = Purchase.objects.filter(student_id=student_id)
        data = []

        for purchase in purchases:
            # find all purchase attendance
            listOfPurchaseAttendance = PurchaseAttendance.objects.filter(
                purchase=purchase)
            purchaseAttendance_data = []

            for purchaseAttendance in listOfPurchaseAttendance:
                purchaseAttendance_data.append(purchaseAttendance.to_json())

            # find all purchase payments
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
                'purchaseAttendance': purchaseAttendance_data,
            }

            data.append(purchase_data)

        return JsonResponse(data, status=201, safe=False)

    except Exception as e:
        response_data = {
            'response_status': 'error',
            'message': str(e)
        }
        return JsonResponse(response_data, status=400, safe=False)


@csrf_exempt
def create_update_purchase(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            purchase_id = data.get('id')

            if purchase_id:
                # Update existing Purchase record
                try:
                    purchase = Purchase.objects.get(id=purchase_id)
                except Purchase.DoesNotExist:
                    return JsonResponse({'success': False, 'message': 'Purchase not found'}, status=404)
            else:
                # Create a new Purchase record
                purchase = Purchase()

            # Update the Purchase object with the fields from the JSON data
            createdBy_data = data.get('createdBy')
            if createdBy_data:
                createdBy_id = createdBy_data.get('id')
                if createdBy_id:
                    try:
                        createdBy = Person.objects.get(id=createdBy_id)
                        purchase.createdBy = createdBy
                    except Person.DoesNotExist:
                        return JsonResponse({'success': False, 'message': 'createdBy not found'}, status=404)

            if not purchase_id:
                purchase.created = timezone.now()

            purchase.lastUpdated = timezone.now()

            lastupdatedby_data = data.get('lastUpdatedBy')
            if lastupdatedby_data:
                lastupdBy_id = lastupdatedby_data.get('id')
                if lastupdBy_id:
                    try:
                        lastupdby = Person.objects.get(id=lastupdBy_id)
                        purchase.lastUpdatedBy = lastupdby
                    except Person.DoesNotExist:
                        return JsonResponse({'success': False, 'message': 'Last updated by not found'}, status=404)

            if data.get('status'):
                purchase.status = data.get('status')

            student_data = data.get('student')
            if student_data:
                student_id = student_data.get('id')
                if student_id:
                    try:
                        student = Person.objects.get(id=student_id)
                        purchase.student = student
                    except Person.DoesNotExist:
                        return JsonResponse({'success': False, 'message': 'Student not found'}, status=404)

            purchase.amount = data.get('amount')
            purchase.maxAttendances = data.get('maxAttendances')

            # Save the Purchase object
            purchase.save()

            response_data = {
                'success': True,
                'message': 'Purchase created/updated successfully'
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
