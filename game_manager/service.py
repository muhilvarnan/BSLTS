import io
import xlsxwriter
from .models import Event, EventMark
from django.db.models import Sum


def get_headers(event):
    headers = ['Zone', 'Code', 'Name of the Participant']
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
                "zone": event_participant.participant.samithi.district.zone.name,
                "code": event_participant.participant.code,
                "name":event_participant.participant.name
            })

        if event_participant.team:
            zones = ",".join(map(lambda participant: participant.samithi.district.zone.name, event_participant.team.participants.all()))
            participants.append({
                "zone": zones,
                "code": event_participant.team.code,
                "name": event_participant.participant.name
            })
    return participants


def get_event_marks(event_participant):
    def get_mark(event_criteria):
        try:
            event_mark = event_participant.eventmark_set.get(event_criteria=event_criteria.id)
            return event_mark.mark
        except EventMark.DoesNotExist:
            return 0
    return list(map(get_mark, event_participant.event.eventcriteria_set.all()))


def get_event_participants_marks(event):
    participant_marks = []
    for event_participant in event.eventparticipant_set.all():
        if event_participant.participant:
            marks = get_event_marks(event_participant)
            participant_marks.append({
                "zone": event_participant.participant.samithi.district.zone.name,
                "code": event_participant.participant.code,
                "marks": marks,
                "total": sum(marks)
            })

        if event_participant.team:
            marks = get_event_marks(event_participant)
            zones = ",".join(map(lambda participant: participant.samithi.district.zone.name, event_participant.team.participants.all()))
            participant_marks.append({
                "zone": zones,
                "code": event_participant.team.code,
                "marks": marks,
                "total": sum(marks)
            })
    return sorted(participant_marks, key = lambda i: i['total'], reverse=True)


def get_end_column_alphabet(header_count):
    return chr(65 + header_count - 1)


def generate_event_rank_sheet(event_id):

    event = Event.objects.get(pk=event_id)

    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    worksheet.set_paper(9)

    header_format = workbook.add_format({'align': 'center', 'bg_color': "orange", 'bold': True, 'border': 1})

    headers = get_headers(event)

    headers.append("Total")

    worksheet.merge_range('A1:%s1' % (get_end_column_alphabet(len(headers))),
                          "Sri Sathya Sai Organisations, Tirupur District, TamilNadu",
                          header_format)

    worksheet.set_column('A:A', 85)

    worksheet.merge_range('A2:%s2' % (get_end_column_alphabet(len(headers))),
                          "TAMILNADU BALVIKAS STATE LEVEL TALENT SEARCH 2019",
                          header_format)

    event_info_format = workbook.add_format({'bold': True, 'font_color': 'red', 'align': 'center'})

    worksheet.merge_range('A3:B3',
                          event.name,
                          event_info_format)

    worksheet.set_column('A3:A3', 30)

    worksheet.merge_range('C3:%s3' % (get_end_column_alphabet(len(headers))),
                          event.group.name,
                          event_info_format)

    row_index = 3

    participants = get_event_participants_marks(event)

    field_header_formatter = workbook.add_format({'bold': True, 'align': 'center'})

    for col_num, header in enumerate(headers):
            worksheet.write(row_index, col_num, header, field_header_formatter)

    worksheet.set_column('A4:B4', 15)

    worksheet.set_column('C4:%s2' % (get_end_column_alphabet(len(headers))), 20)

    row_index = row_index + 1
    for row_num, participant in enumerate(participants):
        worksheet.write(row_index + row_num, 0, participant.get("zone"))
        worksheet.write(row_index + row_num, 1, participant.get("code"))

        column_index = 2
        for event_mark in participant.get("marks"):
            worksheet.write(row_index + row_num, column_index, event_mark)
            column_index = column_index + 1

        worksheet.write(row_index + row_num, column_index, participant.get("total"))

    workbook.close()

    output.seek(0)

    return '%s-%s.xlsx' % (event.group.name, event.name), output


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

    worksheet.merge_range('D3:%s3' % (get_end_column_alphabet(len(headers))),
                          event.group.name,
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
        worksheet.write(row_index + row_num, 0, participant.get("zone"))
        worksheet.write(row_index + row_num, 1, participant.get("code"))
        worksheet.write(row_index + row_num, 2, participant.get("name"))

    workbook.close()

    output.seek(0)

    return '%s-%s.xlsx' % (event.group.name, event.name), output
