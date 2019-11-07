from django.http import HttpResponse
from .service import generate_judge_event_sheet, generate_accommodation_sheet, generate_transportation_sheet
from django.contrib.auth.decorators import login_required


@login_required(login_url='/')
def download_judge_sheet(request, event_id):
    filename, output = generate_judge_event_sheet(event_id)
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

@login_required(login_url='/')
def download_accommodation_count(request, gender):
    filename, output = generate_accommodation_sheet(gender)
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

@login_required(login_url='/')
def download_transportation_count(request, journey_type):
    filename, output = generate_transportation_sheet(journey_type)
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

