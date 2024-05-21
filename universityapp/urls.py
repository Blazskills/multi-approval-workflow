from django.urls import path
from . import views

urlpatterns = [
    path("document/<str:doc_id>",
         views.ApproveDocumentView.as_view(), name="document"),
]
