from django.urls import path
from . import views
from .views import LoginDetailsView, TESTLoginDetailsView

urlpatterns = [
    path("", views.index, name="index"),
    path("login_details.html/", LoginDetailsView.as_view(), name='login_details'), 
    path("login_details_test.html/", TESTLoginDetailsView.as_view(), name='login_details_test'), 
]