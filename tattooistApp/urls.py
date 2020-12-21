from django.urls import path

from . import views

urlpatterns = [
    path("create_portfolio", views.create_portfolio_view, name="create_portfolio"),
    path("create_review/<int:tattooist_id>", views.create_review, name="create_review"),
    path("delete_portfolio/<int:portfolio_id>", views.delete_portfolio, name="delete_portfolio"),
    path("detail_review/<int:review_id>", views.detail_review_view, name="detail_review"),
    path("detail_portfolio/<int:tattooist_id>/<int:portfolio_id>", views.detail_portfolio_view, name="detail_portfolio"),
    path("follow_pressed/<int:tattooist_id>", views.follow_pressed, name="follow_pressed"),
    path("message/<int:customer_id>to<int:tattooist_id>", views.message_view, name="message"),
    path("messagebox/", views.messagebox_view, name="messagebox"),
    path("modify_portfolio/<int:tattooist_id>/<int:portfolio_id>", views.modify_portfolio_view, name="modify_portfolio"),
    path("modify_review_view/<int:tattooist_id>/<int:review_id>", views.modify_review_view,name="modify_review"),
    path("report", views.report_view, name="report"),
    path("tattooist_profile/<int:tattooist_id>", views.tattooist_profile_view, name="tattooist_profile"),
]