from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("booking/<int:route_id>/<str:S_class>/<str:category>/", views.Booking, name="booking_page"),
    path("booking/<int:route_id>/<str:S_class>/<str:category>/payment", views.Payment, name="payment_page"),
    path("booking/<int:route_id>/<str:S_class>/<str:category>/booking_status", views.Booking_status, name="booking_status_page"),
    path("cancellation/", views.Cancel_booking, name="cancellation"),
    path("status/", views.pnr_status, name="pnr_status"),
    path("schedule/", views.train_schedule_lookup, name="schedule"),
    path("passengers/", views.passenger_lookup, name="passenger_lookup"),
    path("TotalRefund/", views.total_refund, name="redfund"),
    path("stats/", views.stats, name="stats"),
    path("admin/", views.admin, name="admin"),
]