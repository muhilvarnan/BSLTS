import io
import xlsxwriter
from .models import Event
from django.db.models import Sum
from django.db import connection




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


def generate_accommodation_sheet(gender):
    participant_gender = 'Boy' if gender == 'male' else 'Girl'
    participant_family_gender = 'Male' if gender == 'male' else 'Female'
    header_gender = 'Gents' if gender == 'male' else 'Mahilas'
    cursor = connection.cursor()

    cursor.execute('''WITH base_table
                        AS (SELECT game_manager_district.NAME,
                                   game_manager_district.contact_name,
                                   game_manager_district.contact_phone_number,
                                   game_manager_participant.id              AS participant_id,
                                   Count(game_manager_participantfamily.id) AS family_count,
                                   CASE when game_manager_participant.gender = '%s' then 1 else null END as gender
                            FROM   game_manager_district
                                   LEFT JOIN game_manager_samithi
                                          ON game_manager_samithi.district_id =
                                             game_manager_district.id
                                   LEFT JOIN game_manager_participant
                                          ON game_manager_participant.samithi_id =
                                             game_manager_samithi.id
                                             AND game_manager_participant.accommodation = true
                                   LEFT JOIN game_manager_participantfamily
                                          ON game_manager_participantfamily.participant_id =
                                             game_manager_participant.id
                                             AND game_manager_participantfamily.gender = '%s'
                            GROUP  BY game_manager_district.NAME,
                                      game_manager_district.contact_name,
                                      game_manager_district.contact_phone_number,
                                      game_manager_participant.id,
                                      game_manager_participant.gender)
                   SELECT NAME,
                          contact_name,
                          contact_phone_number,
  Count(gender) + Sum(family_count) AS count
                          FROM base_table
                   GROUP  BY NAME,
                             contact_name,
                             contact_phone_number; ''' % (participant_gender, participant_family_gender))
    rows = cursor.fetchall()
    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    worksheet.set_paper(9)

    header_format = workbook.add_format({'align': 'center', 'bg_color': "orange", 'bold': True, 'border': 1})

    headers = ['S.No', 'District', 'DEC', 'Contact', 'Count', 'Special Needs', 'Allocation']

    worksheet.merge_range('A1:%s1' % (get_end_column_alphabet(len(headers))),
                          "Aum Sri Sai Ram",
                          header_format)

    worksheet.set_column('A:A', 85)

    worksheet.merge_range('A2:%s2' % (get_end_column_alphabet(len(headers))),
                          "Balvikas State Level Talent Search 2019 : %s Accomdation Details" % header_gender,
                          header_format)

    row_index = 2
    field_header_formatter = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'grey'})

    for col_num, header in enumerate(headers):
        worksheet.write(row_index, col_num, header, field_header_formatter)

    worksheet.set_column('A4:%s4' % (get_end_column_alphabet(len(headers))), 20)

    row_index = row_index + 1
    for row_num, data in enumerate(rows):
        worksheet.write(row_index + row_num, 0, row_num+1)
        worksheet.write(row_index + row_num, 1, data[0])
        worksheet.write(row_index + row_num, 2, data[1])
        worksheet.write(row_index + row_num, 3, data[2])
        worksheet.write(row_index + row_num, 4, data[3])

    workbook.close()

    output.seek(0)

    return 'Accommodation_%s_BSLTS_2019.xlsx'% gender, output


