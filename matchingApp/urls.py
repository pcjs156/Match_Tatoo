from django.urls import path

from . import views

urlpatterns = [
    path("detail_matching/<int:tattooist_id>/<int:matching_id>", views.detail_matching_view, name="detail_matching"),
    path("matching_list", views.matching_list_view, name="matching_list"),
    path("create_matching", views.create_matching_view, name="create_matching"),
    path("modify_matching/<int:tattooist_id>/<int:matching_id>", views.modify_matching_view, name="modify_matching"),
    path("customer_request_rejected", views.customer_request_rejected_view, name="customer_request_rejected"),
]