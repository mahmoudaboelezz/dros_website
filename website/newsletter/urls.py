from django.urls import path
from .views import send_mail_view,send_mail,qr_code,verify_url

app_name = 'newsletter'
urlpatterns = [
    path('', send_mail_view, name='send_mail_view'),
    path('send_mail/', send_mail, name='send_mail'),
    path('verfiy/<str:verfication_code>/', qr_code, name='qr_code'),
    path('verfiy/',verify_url, name='verify'),
]
