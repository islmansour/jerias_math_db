from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from jerias_production.models import Group, GroupEvent, Person
from django.utils import timezone
from datetime import datetime
from django.views.decorators.http import require_GET, require_POST
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
from dateutil import parser
from django.utils.timezone import datetime
from dateutil import parser
from django.utils import timezone
from django.utils.timezone import datetime
from dateutil import parser


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

        # Include related entities in the JSON response
        for result in results:
            group_id = result['group_id']
            created_by_id = result['createdBy_id']
            last_updated_by_id = result['lastUpdatedBy_id']

            group = Group.objects.filter(id=group_id).values(
                'id', 'name', 'startDate', 'endDate', 'weekDays', 'type', 'status', 'createdBy_id', 'lastUpdatedBy_id').first()
            if group:
                teacher_id = group.pop('teacher_id', None)
                if teacher_id:
                    teacher = Person.objects.filter(id=teacher_id).values(
                        'id', 'lastName', 'firstName', 'startDate', 'status', 'phone', 'email', 'parentPhone1', 'parentPhone2', 'dob', 'userId').first()
                    group['teacher'] = teacher

                result['group'] = group

            created_by = Person.objects.filter(id=created_by_id).values(
                'id', 'lastName', 'firstName', 'startDate', 'status', 'phone', 'email', 'parentPhone1', 'parentPhone2', 'dob', 'userId').first()
            if created_by:
                result['createdBy'] = created_by

            last_updated_by = Person.objects.filter(id=last_updated_by_id).values(
                'id', 'lastName', 'firstName', 'startDate', 'status', 'phone', 'email', 'parentPhone1', 'parentPhone2', 'dob', 'userId').first()
            if last_updated_by:
                result['lastUpdatedBy'] = last_updated_by

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
