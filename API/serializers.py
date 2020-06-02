from rest_framework import serializers

from  liveDataApp.models import *


class dailyDataSerializer(serializers.ModelSerializer):

	class Meta:
		model = dailyData
		fields = '__all__'




class TestCounterSerializer(serializers.ModelSerializer):

	class Meta:
		model = TestCounter
		fields = '__all__'




