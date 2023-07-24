from django.http import JsonResponse, StreamingHttpResponse
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


@csrf_exempt
def students_list_stream(request):
    people = Person.objects.filter(type=0)

    def generate_data():
        for person in people:
            yield JsonResponse({
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
                'type': person.type
            })

    response = StreamingHttpResponse(
        generate_data(), content_type='application/json')
    return response


@csrf_exempt
def add_person(request):
    if request.method == 'POST':
        # Retrieve the data from the request body
        data = json.loads(request.body)

        # Retrieve the values using camel case field names
        phone = data['phone']

        try:
            # Try to find the person with the provided phone number
            person = Person.objects.filter(phone=phone).first()

            if person:
                # If the person with the provided phone exists, update their data
                person.lastName = data.get('lastName', person.lastName)
                person.firstName = data.get('firstName', person.firstName)
                person.startDate = data.get('startDate', person.startDate)
                person.status = data.get('status', person.status)
                person.email = data.get('email', person.email)
                person.parentPhone1 = data.get(
                    'parentPhone1', person.parentPhone1)
                person.parentPhone2 = data.get(
                    'parentPhone2', person.parentPhone2)
                person.dob = data.get('dob', person.dob)
                person.userId = data.get('userId', person.userId)
                person.type = data.get('type', person.type)
                person.save()

                response_data = {
                    'response_status': 'success',
                    'message': 'Person updated successfully',
                    'id': person.id,
                }
                return JsonResponse(response_data, status=200, safe=False)
            else:
                # If the person with the provided phone doesn't exist, create a new person
                person = Person.objects.create(
                    phone=phone,
                    lastName=data.get('lastName'),
                    firstName=data.get('firstName'),
                    startDate=data.get('startDate'),
                    status=data.get('status'),
                    email=data.get('email'),
                    parentPhone1=data.get('parentPhone1'),
                    parentPhone2=data.get('parentPhone2'),
                    dob=data.get('dob'),
                    userId=data.get('userId'),
                    type=data.get('type'),
                )

                response_data = {
                    'response_status': 'success',
                    'message': 'Person created successfully',
                    'id': person.id,
                }
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
