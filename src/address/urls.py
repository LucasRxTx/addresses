from django.urls import path

from address import views

urlpatterns = [
    path("", views.AddressList.as_view(), name="address_list"),
    path("<int:pk>/", views.AddressDetail.as_view(), name="address_detail"),
]
