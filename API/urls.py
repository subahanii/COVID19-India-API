

from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.index),
    path('all/', views.all),
    path('stateDataTillDate/', views.getStateDataTillDate),
    path('testDataTillDate/', views.getTestDataTillDate),
    path('testDataOnDate/<str:date>', views.testDataOnDate),
    path('stateDataOnDate/<str:date>', views.stateDataOnDate),
    path('stateAndTestOnDate/<str:date>', views.stateAndTestOnDate),
    path('btwDateSateAndTestData/<str:dates>', views.btwDateSateAndTestData),
   

]