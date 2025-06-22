from django.urls import path, register_converter

from . import converters, views

register_converter(converters.INNConverter, "inn")

urlpatterns = [
    path('webhook/bank/', views.ReceivePaymentView.as_view()),
    path('organizations/<inn:inn>/balance/', views.ReadBalanceView.as_view()),
]





