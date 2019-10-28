from django.urls import path

from . import views

urlpatterns = [
    path('download/judge-sheet/<event_id>', views.download_judge_sheet, name='download_judge_sheet'),
]