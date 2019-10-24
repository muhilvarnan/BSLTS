from django.urls import path

from . import views

urlpatterns = [
    path('download/judge-sheet/<event_id>', views.download_judge_sheet, name='download_judge_sheet'),
    path('download/rank-sheet/<event_id>', views.download_rank_sheet, name='download_rank_sheet'),
]