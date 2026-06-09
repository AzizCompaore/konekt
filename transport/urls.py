from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='home'),
    path('reserver/<int:voyage_id>/', views.reserver_etape_1, name='reserver_etape_1'),
    path('valider/<int:voyage_id>/', views.valider_reservation, name='valider_reservation'),
    path('mes-tickets/', views.mes_tickets, name='mes_tickets'),
    path('ticket/<str:code_ticket>/', views.voir_ticket, name='voir_ticket'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Nouvelle route pour le scan du contrôleur
    path('scan/<str:code_ticket>/', views.valider_ticket_scan, name='valider_ticket_scan'),
    path('agent-control/', views.dashboard_agent, name='dashboard_agent'),
    path('inscription/', views.inscription_view, name='inscription'),
]