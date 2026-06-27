from django.urls import path
from django.views.generic import RedirectView

from textapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/predict-frame/', views.predict_frame),
    # Old routes from previous versions → home page
    path('login/', RedirectView.as_view(url='/', permanent=False)),
    path('userhome/', RedirectView.as_view(url='/', permanent=False)),
    path('prediction/', RedirectView.as_view(url='/', permanent=False)),
    path('imagebyenter/', RedirectView.as_view(url='/', permanent=False)),
    path('udp/', RedirectView.as_view(url='/', permanent=False)),
]
