from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Job
from .serializers import JobSerializer
from .tasks import scrape_coin_data

class StartScrapingView(APIView):
    def post(self, request):
        coins = request.data.get('coins', [])
        if not all(isinstance(coin, str) for coin in coins):
            return Response({'error': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)

        job = Job.objects.create()
        for coin in coins:
            scrape_coin_data(str(job.id), coin)

        return Response({'job_id': job.id}, status=status.HTTP_202_ACCEPTED)

class ScrapingStatusView(APIView):
    def get(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = JobSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)