from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from jerias_production.models import Person, GroupEvent, Purchase, PurchaseAttendance, StudentAttendance
from django.utils import timezone
from dateutil import parser
from dateutil import parser
from django.utils import timezone
from dateutil import parser
from django.db.models import Count


@csrf_exempt
def create_student_attendance(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data
            json_data = json.loads(request.body)
            created = json_data['created']
            last_updated = json_data['lastUpdated']
            student_attendance_id = json_data.get('id')

            if student_attendance_id != -1:
                print('updating exisitng record')
                # If the student_attendance_id is provided, search for the existing object
                student_attendance = StudentAttendance.objects.filter(
                    id=student_attendance_id).first()

                if student_attendance:
                    # If the object exists, perform an update

                    student_attendance.lastUpdated = timezone.now()
                    student_attendance.lastUpdatedBy = json_data['lastUpdatedBy']
                    student_attendance.status = json_data['status']

                    student_attendance.save()
                else:

                    # If the object doesn't exist, return an error response
                    response_data = {
                        'response_status': 'error',
                        'message': f'StudentAttendance object with ID {student_attendance_id} does not exist',
                    }
                    return JsonResponse(response_data, status=404, safe=False)
            else:
                last_updated = timezone.make_aware(parser.parse(last_updated))
                created = timezone.make_aware(parser.parse(created))

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
                    # 'createdBy': group_event.createdBy_id,
                    # 'lastUpdatedBy': group_event.lastUpdatedBy_id,
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

            if(student_attendance_id == -1):
                student_attendances = StudentAttendance.objects.filter(
                    student=student)
                student_attendance_ids = student_attendances.values_list(
                    'id', flat=True)

                purchase_attendances = PurchaseAttendance.objects.filter(
                    studentAttendance__in=student_attendance_ids)

                print(len(purchase_attendances))

            # if len(purchase_attendances) == 0:
                allPurchases = Purchase.objects.filter(student=student)
                selectedPurchase = None
                for purchase in allPurchases:
                    if purchase.noMoreEventsAllowed == False:
                        selectedPurchase = purchase
                        break

                if selectedPurchase:
                    PurchaseAttendance.objects.create(
                        studentAttendance=student_attendance, purchase=selectedPurchase)
                else:
                    selectedPurchase = Purchase.objects.create(
                        amount=0,
                        maxAttendances=8,
                        student=student,
                        autoGenerate=True,
                        status=0,
                        createdBy=None,
                        lastUpdatedBy=None

                    )
                    if selectedPurchase:
                        PurchaseAttendance.objects.create(
                            studentAttendance=student_attendance, purchase=selectedPurchase)

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

                group = attendance.groupEvent.group
                group_data = {
                    'id': group.id,
                    'name': group.name,
                    'startDate': group.startDate,
                    'endDate': group.endDate,
                    'weekDays': group.weekDays,
                    'type': group.type,
                    'status': group.status,
                    # 'createdBy': created_by_data,
                    # 'lastUpdatedBy': last_updated_by_data,
                    # 'teacher': teacher_data
                }
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
                    # 'createdBy': attendance.groupEvent.createdBy_id,
                    # 'lastUpdatedBy': attendance.groupEvent.lastUpdatedBy_id,
                    'group': group_data
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
