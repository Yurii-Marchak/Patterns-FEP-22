# football_events/urls.py
from django.contrib import admin
from django.urls import path
from events.views import fetch_and_save_events
from events import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', fetch_and_save_events, name="fetch_events"),
    path('info/', views.event_info, name='event_info'),  # URL для сторінки з CRUD-функціоналом
    path('info/<int:event_id>/', views.event_info, name='event_info'), 
]
