from django.urls import path
from . import views
from .views import create_team, create_player, edit_salary_cap
urlpatterns = [
    path('', views.home, name='home'),
    path('teams/', views.team_list, name='team_list'),
    path('teams/<int:team_id>/', views.team_detail, name='team_detail'),
    path('players/<int:player_id>/', views.player_detail, name='player_detail'),
    path('new_team/', create_team, name='create_team'),
    path('new_player/', create_player, name='create_player'),
    path('teams/<int:team_id>/edit/', views.edit_team, name='edit_team'),
    path('teams/<int:team_id>/delete/', views.delete_team, name='delete_team'),
    path('players/<int:player_id>/edit/', views.edit_player, name='edit_player'),
    path('players/<int:player_id>/delete/', views.delete_player, name='delete_player'),
    path('edit-salary-cap/', edit_salary_cap, name='edit_salary_cap'),
    # added 
    path('upload_csv/', views.upload_csv, name='upload_csv'),

]
