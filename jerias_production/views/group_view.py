from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from jerias_production.models import Group, GroupPerson, Person
from django.utils import timezone
from django.core import serializers
from django.forms.models import model_to_dict
from dateutil import parser
from dateutil import parser
from django.utils import timezone
from dateutil import parser


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
