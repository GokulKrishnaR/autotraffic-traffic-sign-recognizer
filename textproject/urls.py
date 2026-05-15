from django.urls import path

from textapp import views

urlpatterns = [
    path('', views.home),
    path('api/predict-frame/', views.predict_frame),
]
