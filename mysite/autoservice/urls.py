from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("automobiliai/", views.automobiliai, name="automobiliai"),
    path("automobiliai/<int:auto_id>", views.automobilis, name="automobilis"),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('profilis/', views.profilis, name='profilis'),
    path("uzsakymai/", views.UzsakymasListView.as_view(), name="uzsakymai"),
    path("manouzsakymai/", views.UserUzsakymasListView.as_view(), name="mano_uzsakymai"),
    path("uzsakymai/<int:pk>", views.UzsakymasDetailView.as_view(), name="uzsakymas"),
    path("uzsakymai/sukurti", views.UzsakymasCreateView.as_view(), name="uzsakymas_sukurti"),
    path('uzsakymai/<int:pk>/redaguoti', views.UserUzsakymasUpdateView.as_view(), name="uzsakymas_redaguoti"),
    path('uzsakymai/<int:pk>/istrinti', views.UserUsakymasDeleteView.as_view(), name="uzsakymas_istrinti"),
    path("uzsakymai/<int:pk>/pridetieilute", views.UzsakymoEiluteCreateView.as_view(), name="uzsakymas_pridetieilute"),
    path("uzsakymai/<int:uzsakymas_pk>/redaguotieilute/<int:pk>", views.UzsakymoEiluteUpdateView.as_view(), name="uzsakymas_redaguotieilute"),
    path("uzsakymai/<int:uzsakymas_pk>/istrintieilute/<int:pk>", views.UzsakymoEiluteDeleteView.as_view(), name="uzsakymas_istrintieilute"),
]