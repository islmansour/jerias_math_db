from django.urls import reverse
import requests
from .models import Group, Person, StudentAttendance
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
import json
from django.http import JsonResponse
from jerias_production.models import AppUser, Group, GroupPerson, Person, GroupEvent
from django.utils import timezone
from django.core import serializers
from datetime import datetime
from django.forms.models import model_to_dict
from django.views.decorators.http import require_GET, require_POST
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
from dateutil import parser
from django.db import transaction
from django.utils.timezone import datetime, get_default_timezone
from dateutil import parser
from django.utils import timezone
from django.utils.timezone import datetime
from dateutil import parser


# @csrf_exempt
# def group_list(request):
#     groups = Group.objects.all()
#     try:
#         data = []
#         for group in groups:
#             serialized_teacher = None
#             if group.teacher:
#                 serialized_teacher = {
#                     'id': group.teacher.id,
#                     'lastName': group.teacher.lastName,
#                     'firstName': group.teacher.firstName,
#                     'startDate': group.teacher.startDate,
#                     'status': group.teacher.status,
#                     'phone': group.teacher.phone,
#                     'email': group.teacher.email,
#                     'parentPhone1': group.teacher.parentPhone1,
#                     'parentPhone2': group.teacher.parentPhone2,
#                     'dob': group.teacher.dob,
#                     'userId': group.teacher.userId,
#                 }
#             # else:
#             #     if group.teacherId:
#             #         teacherObject = Person.objects.get(id=group.teacherId)
#             #         serialized_teacher = {
#             #             'id': teacherObject.id,
#             #             'lastName': teacherObject.lastName,
#             #             'firstName': teacherObject.firstName,
#             #             'startDate': teacherObject.startDate,
#             #             'status': teacherObject.status,
#             #             'phone': teacherObject.phone,
#             #             'email': teacherObject.email,
#             #             'parentPhone1': teacherObject.parentPhone1,
#             #             'parentPhone2': teacherObject.parentPhone2,
#             #             'dob': teacherObject.dob,
#             #             'userId': teacherObject.userId,
#             #         }

#             group_data = {
#                 'id': group.id,
#                 'name': group.name,
#                 # 'teacherId': group.teacherId,
#                 'startDate': group.startDate,
#                 'endDate': group.endDate,
#                 'weekDays': group.weekDays,
#                 'type': group.type,
#                 'status': group.status,
#                 'teacher': serialized_teacher,
#             }

#             data.append(group_data)

#         return JsonResponse(data, status=201, safe=False)
#     except Exception as e:
#         response_data = {
#             'response_status': 'error',
#             'message': str(e)
#         }
#         return JsonResponse(response_data, status=400, safe=False)

@csrf_exempt
def group_list(request):
    groups = Group.objects.all()
    try:
        data = []
        for group in groups:
            # Retrieve GroupPerson objects related to the current group
            group_people = GroupPerson.objects.filter(group=group)

            serialized_teacher = None
            if group.teacher:
                serialized_teacher = {
                    'id': group.teacher.id,
                    'lastName': group.teacher.lastName,
                    'firstName': group.teacher.firstName,
                    'startDate': group.teacher.startDate,
                    'status': group.teacher.status,
                    'phone': group.teacher.phone,
                    'email': group.teacher.email,
                    'parentPhone1': group.teacher.parentPhone1,
                    'parentPhone2': group.teacher.parentPhone2,
                    'dob': group.teacher.dob,
                    'userId': group.teacher.userId,
                }

            group_data = {
                'id': group.id,
                'name': group.name,
                'startDate': group.startDate,
                'endDate': group.endDate,
                'weekDays': group.weekDays,
                'type': group.type,
                'status': group.status,
                'teacher': serialized_teacher,
                'groupStudents': []
            }

            for group_person in group_people:
                serialized_student = {
                    'id': group_person.student.id,
                    'lastName': group_person.student.lastName,
                    'firstName': group_person.student.firstName,
                    'startDate': group_person.student.startDate,
                    'status': group_person.student.status,
                    'phone': group_person.student.phone,
                    'email': group_person.student.email,
                    'parentPhone1': group_person.student.parentPhone1,
                    'parentPhone2': group_person.student.parentPhone2,
                    'dob': group_person.student.dob,
                    'userId': group_person.student.userId,
                }
                serialized_group_person = {
                    'id': group_person.id,
                    'studentId': group_person.studentId,
                    'groupId': group_person.groupId,
                    'createdBy': group_person.createdBy.id,
                    'created': group_person.created,
                    'lastUpdated': group_person.lastUpdated,
                    'lastUpdatedBy': group_person.lastUpdatedBy.id,
                    'status': group_person.status,
                    'student': serialized_student
                    # 'group': group_person.group.id,
                    # 'student': group_person.student.id,
                }
              #  serialized_group_person['student'].append(serialized_student)
                group_data['groupStudents'].append(serialized_group_person)

            data.append(group_data)

        return JsonResponse(data, status=201, safe=False)
    except Exception as e:
        response_data = {
            'response_status': 'error',
            'message': str(e)
        }
        return JsonResponse(response_data, status=400, safe=False)


@csrf_exempt
def upsert_group(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            group_id = json_data.get('id')

            print(json_data)

            if group_id:
                # Update existing group
                group = Group.objects.get(id=group_id)
            else:
                # Create a new group
                group = Group()

            # Update the group fields with JSON values
            group.name = json_data.get('name')
            #group.teacherId = json_data.get('teacherId')
            group.startDate = json_data.get('startDate')
            group.endDate = json_data.get('endDate')
            group.weekDays = json_data.get('weekDays')
            group.type = json_data.get('type')
            group.status = json_data.get('status')
            if json_data.get('createdBy'):
                if not group_id:
                    group.createdBy = Person.objects.get(
                        id=json_data.get('createdBy'))

            if json_data.get('lastUpdatedBy'):
                group.lastUpdatedBy = Person.objects.get(
                    id=json_data.get('lastUpdatedBy'))

            # if json_data.get('teacherId'):
            #     group.teacher = Person.objects.get(
            #         id=json_data.get('teacherId'))

            # Set the created and lastUpdated fields
            group.created = timezone.now()
            group.lastUpdated = timezone.now()

            # Save the group record
            group.save()

            # Return the updated or created group data in JSON format
            response_data = {
                'response_status': 'success',
                'message': 'GroupEvent added successfully.',
                'upsert_group': {
                    'id': group.id,
                    'name': group.name,
                    # 'teacherId': group.teacherId,
                    'startDate': group.startDate,
                    'endDate': group.endDate,
                    'weekDays': group.weekDays,
                    'type': group.type,
                    'status': group.status,
                    'createdBy': {
                        'lastName': group.createdBy.lastName if group.createdBy else None,
                        'firstName': group.createdBy.firstName if group.createdBy else None,
                        'startDate': group.createdBy.startDate if group.createdBy else None,
                        'status': group.createdBy.status if group.createdBy else None,
                        'phone': group.createdBy.phone if group.createdBy else None,
                        'email': group.createdBy.email if group.createdBy else None,
                        'parentPhone1': group.createdBy.parentPhone1 if group.createdBy else None,
                        'parentPhone2': group.createdBy.parentPhone2 if group.createdBy else None,
                        'dob': group.createdBy.dob if group.createdBy else None,
                    },
                    'teacher': {
                        'lastName': group.teacher.lastName if group.teacher else None,
                        'firstName': group.teacher.firstName if group.teacher else None,
                        'startDate': group.teacher.startDate if group.teacher else None,
                        'status': group.teacher.status if group.teacher else None,
                        'phone': group.teacher.phone if group.teacher else None,
                        'email': group.teacher.email if group.teacher else None,
                        'parentPhone1': group.teacher.parentPhone1 if group.teacher else None,
                        'parentPhone2': group.teacher.parentPhone2 if group.teacher else None,
                        'dob': group.teacher.dob if group.teacher else None,
                    },
                    'lastUpdatedBy': {
                        'lastName': group.lastUpdatedBy.lastName if group.lastUpdatedBy else None,
                        'firstName': group.lastUpdatedBy.firstName if group.lastUpdatedBy else None,
                        'startDate': group.lastUpdatedBy.startDate if group.lastUpdatedBy else None,
                        'status': group.lastUpdatedBy.status if group.lastUpdatedBy else None,
                        'phone': group.lastUpdatedBy.phone if group.lastUpdatedBy else None,
                        'email': group.lastUpdatedBy.email if group.lastUpdatedBy else None,
                        'parentPhone1': group.lastUpdatedBy.parentPhone1 if group.lastUpdatedBy else None,
                        'parentPhone2': group.lastUpdatedBy.parentPhone2 if group.lastUpdatedBy else None,
                        'dob': group.lastUpdatedBy.dob if group.lastUpdatedBy else None,
                    },
                }
            }

            return JsonResponse(response_data, status=201, safe=False)
        except Exception as e:
            response_data = {
                'response_status': 'error',
                'message': str(e)
            }
            return JsonResponse(response_data, status=400, safe=False)

    response_data = {
        'response_status': 'error',
        'message': str(e)
    }
    return JsonResponse({'error': 'Invalid request method.'}, status=400, safe=False)


@csrf_exempt
def person_list(request):
    people = Person.objects.all()
    try:
        data = [{'id': person.id, 'lastName': person.lastName, 'firstName': person.firstName, 'startDate': person.startDate,
                'status': person.status, 'phone': person.phone, 'email': person.email,
                 'parentPhone1': person.parentPhone1, 'parentPhone2': person.parentPhone2,
                 'dob': person.dob, 'userId': person.userId} for person in people]

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
                userId=user_id
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
                'userId': person.userId
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
                 'admin': app_user.admin, 'person': {
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


@csrf_exempt
def group_person_list(request):
    group_people = GroupPerson.objects.all()
    data = []
    try:
        for gp in group_people:
            serialized_person = serializers.serialize(
                'python', [gp.student])[0]
            serialized_group = serializers.serialize('python', [gp.group])[0]
            serialized_group_teacher = serializers.serialize(
                'python', [gp.group.teacher])[0]

            serialized_gp = {
                'id': gp.id,
                'studentId': gp.studentId,
                'groupId': gp.groupId,
                'createdBy': gp.createdBy_id,
                'created': gp.created,
                'lastUpdated': gp.lastUpdated,
                'lastUpdatedBy': gp.lastUpdatedBy_id,
                'status': gp.status,
                'group': {
                    'id': serialized_group['pk'],
                    'name': serialized_group['fields']['name'],
                    'startDate': serialized_group['fields']['startDate'],
                    'endDate': serialized_group['fields']['endDate'],
                    'weekDays': serialized_group['fields']['weekDays'],
                    'type': serialized_group['fields']['type'],
                    'status': serialized_group['fields']['status'],
                    'teacher': {
                        'id': serialized_group_teacher['pk'],
                        'lastName': serialized_group_teacher['fields']['lastName'],
                        'firstName': serialized_group_teacher['fields']['firstName'],
                        # Include any other fields you want from the teacher model
                    }
                },
                'student': {
                    'id': serialized_person['pk'],
                    'lastName': serialized_person['fields']['lastName'],
                    'firstName': serialized_person['fields']['firstName'],
                    'startDate': serialized_person['fields']['startDate'],
                    'status': serialized_person['fields']['status'],
                    'phone': serialized_person['fields']['phone'],
                    'email': serialized_person['fields']['email'],
                    'parentPhone1': serialized_person['fields']['parentPhone1'],
                    'parentPhone2': serialized_person['fields']['parentPhone2'],
                    'dob': serialized_person['fields']['dob'],
                    'userId': serialized_person['fields']['userId'],
                }
            }
            data.append(serialized_gp)
        return JsonResponse(data, status=201, safe=False)

    except Exception as e:
        response_data = {
            'response_status': 'error',
            'message': str(e)
        }
        return JsonResponse(response_data, status=400, safe=False)


@csrf_exempt
def create_group_person(request):
    if request.method == 'POST':
        # Retrieve the data from the request JSON body
        data = json.loads(request.body)

        try:
            # created = datetime.strptime(
            #     data['created'], '%Y-%m-%dT%H:%M:%S.%f')
            # last_updated = datetime.strptime(
            #     data['lastUpdated'], '%Y-%m-%dT%H:%M:%S.%f')
            created = parser.parse(data['created'])
            last_updated = parser.parse(data['lastUpdated'])

            # # Convert the datetime objects to the default timezone
            # created = timezone.make_aware(created, get_default_timezone())
            # last_updated = timezone.make_aware(
            #     last_updated, get_default_timezone())

            group_person = GroupPerson.objects.create(
                studentId=data['studentId'],
                groupId=data['groupId'],
                createdBy=Person.objects.get(id=data['createdBy']),
                created=timezone.make_aware(created),
                lastUpdated=timezone.make_aware(last_updated),
                lastUpdatedBy=Person.objects.get(id=data['lastUpdatedBy']),
                status=data['status'],
                group=Group.objects.get(id=data['groupId']),
                student=Person.objects.get(id=data['studentId'])
            )

            # Convert GroupPerson object to dictionary
            group_person_dict = model_to_dict(group_person)
            group_person_dict['group'] = model_to_dict(group_person.group)
            group_person_dict['group']['teacher'] = model_to_dict(
                group_person.group.teacher)

            group_person_dict['student'] = model_to_dict(group_person.student)

            # Return the JSON response with the created data and success status
            response_data = {
                'response_status': 'success',
                'group_person': group_person_dict
            }
            print(group_person_dict)
            return JsonResponse(response_data, status=201)

        except Exception as e:
            # Return the JSON response with error status and error message
            response_data = {
                'response_status': 'error',
                'message': str(e)
            }
            return JsonResponse(response_data, status=400)

        except (KeyError, Person.DoesNotExist, Group.DoesNotExist):
            return JsonResponse({'error': 'Invalid data'}, status=400)

    # Handle other HTTP methods
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@require_GET
def search_group_events(request):
    try:
        group_id = request.GET.get('group_id')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        queryset = GroupEvent.objects.all().order_by('-created')

        if group_id:
            queryset = queryset.filter(group_id=group_id)

        if from_date:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            queryset = queryset.filter(created__gte=from_date)

        if to_date:
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
            queryset = queryset.filter(created__lte=to_date)

        results = list(queryset.values('id', 'created', 'lastUpdated',
                       'status', 'group_id', 'createdBy_id', 'lastUpdatedBy_id'))

        return JsonResponse(results, status=201, safe=False)
    except Exception as e:
        response_data = {
            'response_status': 'error',
            'message': str(e)
        }
        return JsonResponse(response_data, status=400, safe=False)


@csrf_exempt
@require_POST
def add_group_event(request):
    try:
        # Parse the JSON data from the request body
        json_data = json.loads(request.body)

        # Extract the required fields from the JSON data
        created = json_data['created']
        last_updated = json_data['lastUpdated']

        created = timezone.make_aware(parser.parse(created))
        last_updated = timezone.make_aware(parser.parse(last_updated))
        status = json_data.get('status')
        created_by_id = json_data.get('createdBy')
        last_updated_by_id = json_data.get('lastUpdatedBy')
        group_id = json_data.get('group', {}).get('id')
        groupData = json_data.get('group')

        # Perform additional validations or processing as needed

        # Create the GroupEvent instance
        group_event = GroupEvent.objects.create(
            created=created,
            lastUpdated=last_updated,
            status=status,
            createdBy_id=created_by_id,
            lastUpdatedBy_id=last_updated_by_id,
            group_id=group_id
        )

        # Return a JSON response with the created GroupEvent data
        group_event_result = {
            'id': group_event.id,
            'created': group_event.created,
            'lastUpdated': group_event.lastUpdated,
            'status': group_event.status,
            'createdBy': group_event.createdBy_id,
            'lastUpdatedBy': group_event.lastUpdatedBy_id,
            'group': groupData
        }

        response_data = {
            'response_status': 'success',
            'message': 'group_event object created successfully',
            'group_event': group_event_result
        }

        return JsonResponse(response_data, status=201, safe=False)
    except Exception as e:
        response_data = {
            'response_status': 'error',
            'message': str(e)
        }
        return JsonResponse(response_data, status=400, safe=False)


class StudentAttendanceEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, StudentAttendance):
            # Convert StudentAttendance object to a dictionary
            return {
                'id': obj.id,
                'createdBy': obj.createdBy,
                'created': obj.created,
                'lastUpdated': obj.lastUpdated,
                'lastUpdatedBy': obj.lastUpdatedBy,
                'status': obj.status,
                'groupEvent': obj.groupEvent,
                'student': obj.student,
            }
        return super().default(obj)


class GroupEventEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, GroupEvent):
            # Convert GroupEvent object to a dictionary
            return {
                'id': obj.id,
                'createdBy': obj.createdBy,
                'created': obj.created,
                'lastUpdated': obj.lastUpdated,
                'lastUpdatedBy': obj.lastUpdatedBy,
                'status': obj.status,
                'group': obj.group,
            }
        return super().default(obj)


@csrf_exempt
def create_student_attendance(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data
            json_data = json.loads(request.body)
            created = json_data['created']
            last_updated = json_data['lastUpdated']

            created = timezone.make_aware(parser.parse(created))
            last_updated = timezone.make_aware(parser.parse(last_updated))

            # Create a new StudentAttendance object
            student_attendance = StudentAttendance.objects.create(
                createdBy=json_data['createdBy'],
                created=created,
                lastUpdated=last_updated,
                lastUpdatedBy=json_data['lastUpdatedBy'],
                status=json_data['status'],
                groupEvent_id=json_data['groupEvent']['id'],
                student_id=json_data['student']['id']
            )

            # Fetch the object again to get the updated data including the id
            student_attendance.refresh_from_db()

            # Fetch the student object
            student = Person.objects.get(pk=json_data['student']['id'])
            group_event = GroupEvent.objects.get(
                pk=json_data['groupEvent']['id'])

            # Serialize the StudentAttendance and GroupEvent objects
            serialized_student_attendance = {
                'id': student_attendance.id,
                'createdBy': student_attendance.createdBy,
                'created': student_attendance.created,
                'lastUpdated': student_attendance.lastUpdated,
                'lastUpdatedBy': student_attendance.lastUpdatedBy,
                'status': student_attendance.status,
                'groupEvent': student_attendance.groupEvent_id,
                'groupEvent': {
                    'id': group_event.id,
                    'created': group_event.created,
                    'lastUpdated': group_event.lastUpdated,
                    'status': group_event.status,
                    'createdBy': group_event.createdBy_id,
                    'lastUpdatedBy': group_event.lastUpdatedBy_id,
                    # 'group': group_event.group_id,
                },
                'student': {
                    'id': student.id,
                    'lastName': student.lastName,
                    'firstName': student.firstName,
                    'startDate': student.startDate,
                    'status': student.status,
                    'phone': student.phone,
                    'email': student.email,
                    'parentPhone1': student.parentPhone1,
                    'parentPhone2': student.parentPhone2,
                    'dob': student.dob,
                    'userId': student.userId
                }
            }
            # serialized_group_event = serializers.serialize(
            #     'python', [GroupEvent])[0]['fields']

            response_data = {
                'response_status': 'success',
                'message': 'StudentAttendance object created successfully',
                'student_attendance': serialized_student_attendance,
                #   'group_event': serialized_group_event,
            }

            return JsonResponse(response_data, status=201, safe=False)

        except Exception as e:
            response_data = {
                'response_status': 'error',
                'message': str(e),
            }
            return JsonResponse(response_data, status=400, safe=False)

    return JsonResponse({'error': 'Invalid request method'}, status=400, safe=False)


@csrf_exempt
def get_student_attendance_by_group_event(request):
    if request.method == 'GET':
        try:
            group_event_id = request.GET.get('groupEvent_id')

            # Retrieve all StudentAttendance records filtered by GroupEvent
            student_attendance_list = StudentAttendance.objects.filter(
                groupEvent_id=group_event_id)

            # Create a list of dictionaries containing the data of each StudentAttendance object
            student_attendance_data = []
            for attendance in student_attendance_list:
                student_data = {
                    'id': attendance.student.id,
                    'lastName': attendance.student.lastName,
                    'firstName': attendance.student.firstName,
                    'startDate': attendance.student.startDate,
                    'status': attendance.student.status,
                    'phone': attendance.student.phone,
                    'email': attendance.student.email,
                    'parentPhone1': attendance.student.parentPhone1,
                    'parentPhone2': attendance.student.parentPhone2,
                    'dob': attendance.student.dob,
                    'userId': attendance.student.userId
                }
                group_event_data = {
                    'id': attendance.groupEvent.id,
                    'created': attendance.groupEvent.created,
                    'lastUpdated': attendance.groupEvent.lastUpdated,
                    'status': attendance.groupEvent.status,
                    'createdBy': attendance.groupEvent.createdBy_id,
                    'lastUpdatedBy': attendance.groupEvent.lastUpdatedBy_id,
                    # 'group': attendance.groupEvent.group_id,
                }
                attendance_data = {
                    'id': attendance.id,
                    'createdBy': attendance.createdBy,
                    'created': attendance.created,
                    'lastUpdated': attendance.lastUpdated,
                    'lastUpdatedBy': attendance.lastUpdatedBy,
                    'status': attendance.status,
                    'groupEvent': group_event_data,
                    'student': student_data
                }
                student_attendance_data.append(attendance_data)

            response_data = {
                'response_status': 'success',
                'message': 'StudentAttendance objects retrieved successfully',
                'student_attendance': student_attendance_data
            }
            return JsonResponse(student_attendance_data, status=201, safe=False)

        except Exception as e:
            response_data = {
                'response_status': 'error',
                'message': str(e)
            }
            return JsonResponse(response_data, status=400, safe=False)

    return JsonResponse({'error': 'Invalid request method'}, safe=False)


@csrf_exempt
def search_student_attendance_by_student(request):
    if request.method == 'GET':
        student_id = request.GET.get('student_id')

        # Search for StudentAttendance records based on the provided student
        try:
            student_attendance_list = StudentAttendance.objects.filter(
                student_id=student_id)

            # Create a list of dictionaries containing the data of each StudentAttendance object
            student_attendance_data = []
            for attendance in student_attendance_list:
                student_data = {
                    'id': attendance.student.id,
                    'lastName': attendance.student.lastName,
                    'firstName': attendance.student.firstName,
                    'startDate': attendance.student.startDate,
                    'status': attendance.student.status,
                    'phone': attendance.student.phone,
                    'email': attendance.student.email,
                    'parentPhone1': attendance.student.parentPhone1,
                    'parentPhone2': attendance.student.parentPhone2,
                    'dob': attendance.student.dob,
                    'userId': attendance.student.userId
                }
                attendance_data = {
                    'id': attendance.id,
                    'createdBy': attendance.createdBy,
                    'created': attendance.created,
                    'lastUpdated': attendance.lastUpdated,
                    'lastUpdatedBy': attendance.lastUpdatedBy,
                    'status': attendance.status,
                    'groupEvent': attendance.groupEvent.id,
                    'student': student_data
                }
                student_attendance_data.append(attendance_data)

            response_data = {
                'response_status': 'success',
                'message': 'StudentAttendance objects retrieved successfully',
                'student_attendance': student_attendance_data
            }
            return JsonResponse(response_data, status=200, safe=False)

        except Exception as e:
            response_data = {
                'response_status': 'error',
                'message': str(e)
            }
            return JsonResponse(response_data, status=400, safe=False)

    return JsonResponse({'error': 'Invalid request method'}, safe=False)
