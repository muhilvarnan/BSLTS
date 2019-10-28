import io
import xlsxwriter
from .models import Event
from django.db.models import Sum


def get_headers(event):
    headers = ['Code', 'Name of the Participant']
    for eventCriteria in event.eventcriteria_set.all():
        headers.append('%s(%s)' % (eventCriteria.name, eventCriteria.max_mark))
    total = event.eventcriteria_set.all().aggregate(Sum('max_mark'))
    headers.append('Total(%s)' % (total.get('max_mark__sum')))

    return headers


def get_event_participants(event):
    participants = []
    for event_participant in event.eventparticipant_set.all():
        if event_participant.participant:
            participants.append({
                "code": event_participant.participant.code,
                "name": event_participant.participant.name
            })

        if event_participant.team:
            participants.append({
                "code": event_participant.team.code,
                "name": "\n".join(map(lambda participant: participant.name,event_participant.team.participants.all()))
            })
    return participants


def get_end_column_alphabet(header_count):
    return chr(65 + header_count - 1)


def generate_judge_event_sheet(event_id):

    event = Event.objects.get(pk=event_id)

    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    worksheet.set_paper(9)

    header_format = workbook.add_format({'align': 'center', 'bg_color': "orange", 'bold': True, 'border': 1})

    headers = get_headers(event)

    worksheet.merge_range('A1:%s1' % (get_end_column_alphabet(len(headers))),
                          "Sri Sathya Sai Organisations, Tirupur District, TamilNadu",
                          header_format)

    worksheet.set_column('A:A', 85)

    worksheet.merge_range('A2:%s2' % (get_end_column_alphabet(len(headers))),
                          "TAMILNADU BALVIKAS STATE LEVEL TALENT SEARCH 2019",
                          header_format)

    event_info_format = workbook.add_format({'bold': True, 'font_color': 'red', 'align': 'center'})

    worksheet.merge_range('A3:C3',
                          event.name,
                          event_info_format)

    worksheet.set_column('A3:A3', 30)

    group_name = " - ".join(map(lambda group: group.name, event.groups.all()))

    worksheet.merge_range('D3:%s3' % (get_end_column_alphabet(len(headers))),
                          group_name,
                          event_info_format)

    row_index = 3

    participants = get_event_participants(event)

    field_header_formatter = workbook.add_format({'bold': True, 'align': 'center'})

    for col_num, header in enumerate(headers):
        worksheet.write(row_index, col_num, header, field_header_formatter)

    worksheet.set_column('A4:B4', 15)

    worksheet.set_column('C4:%s2' % (get_end_column_alphabet(len(headers))), 20)

    row_index = row_index + 1
    for row_num, participant in enumerate(participants):
        worksheet.write(row_index + row_num, 0, participant.get("code"))
        worksheet.write(row_index + row_num, 1, participant.get("name"))

    workbook.close()

    output.seek(0)

    return '%s-%s.xlsx' % (group_name, event.name), output
