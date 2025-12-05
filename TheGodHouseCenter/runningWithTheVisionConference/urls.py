from django.urls import path
from .views import RegistrationView, MomentUploadView, MomentListView

app_name="rvc"
urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("moments/", MomentUploadView.as_view(), name="moments"),
    path("moments/list/", MomentListView.as_view(), name="moments-list"),
]
