# urls.py

from django.urls import path
from .views import InitView ,OutputView
urlpatterns = [
    path('rest/calendar/init/', InitView.as_view(), name='calendar-init'),
    path('rest/calendar/redirect/', OutputView.as_view(), name='calendar-redirect'),

]
