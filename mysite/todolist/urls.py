from django.urls import path
from . import views
from .views import UzduotysList, UzduotisDetail, VartotojoUzduotysDetail, VartotojoUzduotisList, UzduotisVartotojoCreate, UzduotisVartotojoUpdate, UzduotisVartotojoDelete


urlpatterns = [
    path("", views.index, name="index"),
    path('register/', views.register, name='register'),
    path("uzduotys/", UzduotysList.as_view(), name="uzduotys"),
    path('uzduotys/<int:pk>/', UzduotisDetail.as_view(), name='uzduotis'),
    path("vartotojouzduotys/", VartotojoUzduotisList.as_view(), name="vartotojo_uzduotys"),
    path('vartotojouzduotys/<int:pk>', VartotojoUzduotysDetail.as_view(), name='vartotojo-uzduotys'),
    path('uzduotis_sukurti/', UzduotisVartotojoCreate.as_view(), name='uzduotis_sukurti'),
    path('uzduotis_redaguoti/<int:pk>/', UzduotisVartotojoUpdate.as_view(), name='uzduotis_redaguoti'),
    path('uzduotis_trinti/<int:pk>/', UzduotisVartotojoDelete.as_view(), name='uzduotis_trinti'),

]