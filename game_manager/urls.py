from django.urls import path

from . import views

urlpatterns = [
    path('download/judge-sheet/<event_id>', views.download_judge_sheet, name='download_judge_sheet'),
    path('download/district/<gender>/accommodation-count', views.download_accommodation_count, name='download_accommodation_count'),
    path('download/district/<journey_type>/transportation-count', views.download_transportation_count, name='download_transportation_count'),
]