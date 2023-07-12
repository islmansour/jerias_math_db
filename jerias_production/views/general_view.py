from django.http import JsonResponse

from jerias_production.models import LookupTable


def get_lookup_table_data(request):
    try:
        lookup_table_data = LookupTable.objects.all()
        data_json = [data.to_json() for data in lookup_table_data]
        return JsonResponse(data_json, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
