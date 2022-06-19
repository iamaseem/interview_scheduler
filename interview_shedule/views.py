from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from .models import Schedule
from .serializers import ScheduleSerializer
from rest_framework.decorators import api_view

from .utils import convert_to_24_format
from datetime import datetime, timedelta


@api_view(['POST'])
def schedule_add_or_get(request):
  if request.method == 'POST':
    time_format = "%I:%M %p"
    schedule_data = JSONParser().parse(request)
    try:
      datetime.strptime(schedule_data['from_time'], time_format)
      datetime.strptime(schedule_data['to_time'], time_format)
    except ValueError:
      return JsonResponse('Time format is not supported.', status=status.HTTP_400_BAD_REQUEST, safe=False)
    schedule_serializer = ScheduleSerializer(data=schedule_data)
    if schedule_serializer.is_valid():
      schedule_serializer.save()
      return JsonResponse(schedule_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(schedule_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  else:
    return JsonResponse('This method is not allowed.', status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def check(request):
  if request.method == 'POST':
    try:
      time_format = '%H:%M'
      check_data = JSONParser().parse(request)
      candidate_email = check_data['candidateEmailId']
      interviewer_email = check_data['interviewEmailId']
      candidate_data = Schedule.objects.filter(email=candidate_email).order_by('created_at').first()
      interviewer_data = Schedule.objects.filter(email=interviewer_email).order_by('created_at').first()
      if(not interviewer_data and not candidate_data):
        return JsonResponse('Email of candidate/interviewer is wrong.', status=status.HTTP_200_OK, safe=False)
      interviewer_from_time = datetime.strptime(convert_to_24_format(interviewer_data.from_time), time_format)
      interviewer_to_time = datetime.strptime(convert_to_24_format(interviewer_data.to_time), time_format)
      candidate_from_time = datetime.strptime(convert_to_24_format(candidate_data.from_time), time_format)
      candidate_to_time = datetime.strptime(convert_to_24_format(candidate_data.to_time), time_format)
      starting_time = ''
      ending_time = ''
      if(interviewer_from_time > candidate_from_time):
        starting_time = interviewer_from_time
      else:
        starting_time = candidate_from_time

      if(interviewer_to_time < candidate_to_time):
        ending_time = interviewer_to_time
      else:
        ending_time = candidate_to_time

      total_hour_available = int((ending_time - starting_time).total_seconds() / 3600)
      available_schedule = []
      while(total_hour_available):
        if(starting_time.hour < ending_time.hour):
          available_schedule.append((datetime.strftime(starting_time, '%I:%M %p'), datetime.strftime(starting_time+timedelta(hours=1), '%I:%M %p')))
        starting_time += timedelta(hours=1)
        total_hour_available -= 1

      return JsonResponse(available_schedule, status=status.HTTP_200_OK, safe=False)
    except:
      return JsonResponse('Something went wrong', status=status.HTTP_200_OK, safe=False)
  else:
    return JsonResponse('This method is not allowed.', status=status.HTTP_400_BAD_REQUEST, safe=False)