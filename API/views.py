from django.shortcuts import render

from django.http import HttpResponse

from django.shortcuts import get_object_or_404

#from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from  liveDataApp.models import *
from . serializers import *
from rest_framework.decorators import api_view
from datetime import date
import datetime 
from django.db.models import Count
from collections import defaultdict as dfd



def index(request):
	return render(request,'api.html')

def MakingJson(stateDatabase,testDatabase):
	allData = dfd(list)
	allDataAndTest = dfd(list)
	allTestData = dfd(int)
	
	for data in testDatabase:
		date = str(data.when)
		splitDate = date.split(' ')[0]
		allTestData[splitDate]=data.tests



	for state in stateDatabase:
		date = str(state.when)
		splitDate = date.split(' ')[0]
			
		allData[splitDate].append({'stateName':state.stateName, 'confirmedCases':state.confirmedCases,
			'curedCases':state.curedCases, 'deathCases':state.deathCases})


	for date in allData:
		test=0
		if date in allTestData:
			test = allTestData[date]

		allDataAndTest[date].append({'test':test})
		allDataAndTest[date].append({'data':allData[date]})

	return allDataAndTest




def MakingJson2(stateDatabase):
	allData = dfd(list)
	allDataAndTest = dfd(list)
	allTestData = dfd(int)
	
	# for data in testDatabase:
	# 	date = str(data.when)
	# 	splitDate = date.split(' ')[0]
	# 	allTestData[splitDate]=data.tests



	for state in stateDatabase:
		date = str(state.when)
		splitDate = date.split(' ')[0]
			
		allData[splitDate].append({'stateName':state.stateName, 'confirmedCases':state.confirmedCases,
			'curedCases':state.curedCases, 'deathCases':state.deathCases})


	for date in allData:
		# test=0
		# if date in allTestData:
		# 	test = allTestData[date]

		# allDataAndTest[date].append({'test':test})
		allDataAndTest[date].append({'data':allData[date]})

	return allDataAndTest


@api_view(['GET'])
def all(request):

	if request.method == 'GET':
		#print('all')
		stateDatabase = dailyData.objects.all( )
		testDatabase = TestCounter.objects.all()
		#data = dailyData.objects.filter(when__range=['2020-04-01', date.today()]  )
		allData = MakingJson(stateDatabase,testDatabase)

		return Response(data=allData)
		

  
  

@api_view(['GET'])
def getStateDataTillDate(request):
	if request.method == 'GET':
		#print("heloo")
		stateDatabase = dailyData.objects.all()

		#dailyData1 = dailyData.objects.all()
		#serializer = dailyDataSerializer(dailyData1, many=True)	
		#return Response(serializer.data)
		allData = MakingJson2(stateDatabase)

		return Response(data=allData)
  


@api_view(['GET'])
def getTestDataTillDate(request):
	if request.method == 'GET':
		#TestCounter1 = TestCounter.objects.all()
		# serializer = TestCounterSerializer(TestCounter1, many=True)	
		# return Response(serializer.data)
		
		testDatabase = TestCounter.objects.all()
		allTestData = dfd(int)
		for data in testDatabase:
			date = str(data.when)
			splitDate = date.split(' ')[0]
			allTestData[splitDate]=data.tests
		return Response(data=allTestData)
  

@api_view(['GET'])
def testDataOnDate(request,date):
	if request.method == 'GET':
		#print('get')
		try:
			splitDate1 = list(map(int,date.split('-')))
			splitDate = list(map(str,date.split('-')))
			#print(splitDate)
			if len(splitDate)!=3:
				return Response(data={'status':'Wrong Date Format'})

		except:
			return Response(data={'status':'Wrong Date Format'})

		data = TestCounter.objects.filter(when__year=splitDate[0], when__month=splitDate[1], when__day=splitDate[2] )
		serializer = TestCounterSerializer(data, many=True)
		return Response(serializer.data)
  
 
@api_view(['GET'])
def stateDataOnDate(request,date):
	if request.method == 'GET':
		#print('get')
		try:
			splitDate1 = list(map(int,date.split('-')))
			splitDate = list(map(str,date.split('-')))
			#print(splitDate)
			if len(splitDate)!=3:
				return Response(data={'status':'Wrong Date Format'})

		except:
			return Response(data={'status':'Wrong Date Format'})

		data = dailyData.objects.filter(when__year=splitDate[0], when__month=splitDate[1], when__day=splitDate[2] )
		serializer = dailyDataSerializer(data, many=True)
		return Response(serializer.data)




@api_view(['GET'])
def stateAndTestOnDate(request,date):
	if request.method == 'GET':
		try:
			splitDate1 = list(map(int,date.split('-')))
			splitDate = list(map(str,date.split('-')))
			#print(splitDate)
			if len(splitDate)!=3:
				return Response(data={'status':'Wrong Date Format'})

		except:
			return Response(data={'status':'Wrong Date Format'})


		stateDatabase = dailyData.objects.filter(when__year=splitDate[0], when__month=splitDate[1], when__day=splitDate[2] )
		testDatabase = TestCounter.objects.filter(when__year=splitDate[0], when__month=splitDate[1], when__day=splitDate[2] )
		

		allData = MakingJson(stateDatabase,testDatabase)

		return Response(data=allData)

@api_view(['GET'])
def btwDateSateAndTestData(request,dates):
	if request.method == 'GET':
		try:
			splitTwoDate = list(map(str,dates.split('to')))
			#print(splitTwoDate)

			if len(splitTwoDate)==2:
				startDate1 = list(map(int,splitTwoDate[0].split('-')))
				startDate = list(map(str,splitTwoDate[0].split('-')))


				endDate1 = list(map(int,splitTwoDate[1].split('-')))
				endDate = list(map(str,splitTwoDate[1].split('-')))

				#print('2')
				#print(startDate)
				if len(startDate)!=3 and len(endDate)!=3:
					return Response(data={'status':'Wrong Date Format1'})
			else:
				return Response(data={'status':'Wrong Date Format2'})

		except:
			return Response(data={'status':'Wrong Date Format3'})

		stateDatabase = dailyData.objects.filter(when__gte=datetime.date(startDate1[0], startDate1[1], startDate1[2]),when__lte=datetime.date(endDate1[0], endDate1[1], endDate1[2]))
		testDatabase = TestCounter.objects.filter(when__gte=datetime.date(startDate1[0], startDate1[1], startDate1[2]),when__lte=datetime.date(endDate1[0], endDate1[1], endDate1[2]))
		#dailyData.objects.filter(when__gte=datetime.date(2011, 1, 1),when__lte=datetime.date(2011, 1, 31))

		allData = MakingJson(stateDatabase,testDatabase)

		return Response(data=allData)

  
 