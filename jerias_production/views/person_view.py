from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from django.http import JsonResponse
from jerias_production.models import AppUser, Person


@csrf_exempt
def person_list(request):
    people = Person.objects.all()
    try:
        data = [{'id': person.id, 'lastName': person.lastName, 'firstName': person.firstName, 'startDate': person.startDate,
                'status': person.status, 'phone': person.phone, 'email': person.email,
                 'parentPhone1': person.parentPhone1, 'parentPhone2': person.parentPhone2,
                 'dob': person.dob, 'userId': person.userId, 'type': person.type} for person in people]

        return JsonResponse(data, status=201, safe=False)

    except Exception as e:
        response_data = {
            'response_status': 'error',
            'message': str(e)
        }
        return JsonResponse(response_data, status=400, safe=False)


def add_person(request):
    if request.method == 'POST':
        # Retrieve the data from the request body
        data = json.loads(request.body)

        # Retrieve the values using camel case field names
        last_name = data['lastName']
        first_name = data['firstName']
        start_date = data['startDate']
        status = data['status']
        phone = data['phone']
        email = data['email']
        parent_phone1 = data['parentPhone1']
        parent_phone2 = data['parentPhone2']
        dob = data['dob']
        user_id = data['userId']
        type = data['type']

        try:
            # Create a new Person instance with the provided data
            person = Person.objects.create(
                lastName=last_name,
                firstName=first_name,
                startDate=start_date,
                status=status,
                phone=phone,
                email=email,
                parentPhone1=parent_phone1,
                parentPhone2=parent_phone2,
                dob=dob,
                userId=user_id,
                type=type
            )

            # Create a JSON object containing the created data and success status
            response_data = {
                'response_status': 'success',
                'id': person.id,
                'lastName': person.lastName,
                'firstName': person.firstName,
                'startDate': person.startDate,
                'status': person.status,
                'phone': person.phone,
                'email': person.email,
                'parentPhone1': person.parentPhone1,
                'parentPhone2': person.parentPhone2,
                'dob': person.dob,
                'userId': person.userId,
                'type': person.type,
            }

            # Return the JSON response with the created data and success status
            return JsonResponse(response_data, status=201, safe=False)

        except Exception as e:
            # Return the JSON response with error status and error message
            response_data = {
                'response_status': 'error',
                'message': str(e)
            }
            return JsonResponse(response_data, status=400, safe=False)

            # Render the form template for adding a person
    return HttpResponse('empty')


@csrf_exempt
def app_user_list(request):
    app_users = AppUser.objects.all()
    try:
        data = [{'uid': app_user.uid, 'token': app_user.token, 'active': app_user.active,
                'contactId': app_user.contactId, 'created_by': app_user.created_by,
                 'userType': app_user.userType, 'language': app_user.language,
                 'admin': app_user.admin, 'person': {'type': app_user.person.type,
                                                     'lastName': app_user.person.lastName, 'firstName': app_user.person.firstName,
                                                     'startDate': app_user.person.startDate, 'status': app_user.person.status,
                                                     'phone': app_user.person.phone, 'email': app_user.person.email,
                                                     'parentPhone1': app_user.person.parentPhone1, 'parentPhone2': app_user.person.parentPhone2,
                                                     'dob': app_user.person.dob, 'userId': app_user.person.userId
                                                     }} for app_user in app_users]
        return JsonResponse(data, status=201, safe=False)

    except Exception as e:
        response_data = {
            'response_status': 'error',
            'message': str(e)
        }
        return JsonResponse(response_data, status=400, safe=False)
