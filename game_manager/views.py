from django.http import HttpResponse
from .service import generate_judge_event_sheet
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

