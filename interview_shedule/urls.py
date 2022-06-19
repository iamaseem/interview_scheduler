from django.urls import path
from interview_shedule import views

urlpatterns = [
  path('schedule/', views.schedule_add_or_get),
  path('check/', views.check)
]