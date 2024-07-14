from django.urls import path
from .views import *

urlpatterns = [
    path('home/', home, name='home'),
    path('page/', page, name='page'),
    path('predict/', predict, name='predict'),
    path('save_feedback/', save_feedback, name='save_feedback'),
    path('signup', signup, name='signup'),
    path('logout', logout, name='logout'),
        path('', login, name='login'),

]