from django.urls import path
from . import views



app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('user/login/', views.LoginView.as_view(), name='user_login'),
    path('user/logout/', views.LogoutView.as_view(), name='user_logout'),
    path('user/register/', views.RegisterView.as_view(), name='user_register'),

    path('add/location/', views.AddLocationView.as_view(), name='add_location'),
    path('add/session/', views.AddSessionView.as_view(), name='add_session'),
    path('add/customer/', views.AddCustomerView.as_view(), name='add_customer'),

    path('datail/session/<int:session_id>/', views.SessionDetailView.as_view(), name='session_detail'),
    path('datail/location/<int:location_id>/', views.LocationDetailView.as_view(), name='location_detail'),
    path('datail/customer/<int:customer_id>/', views.CustomerDetailView.as_view(), name='customer_detail'),

    path('list/location/', views.LocationListView.as_view(), name='location_list'),
    path('list/session/', views.SessionListView.as_view(), name='session_list'),
    path('list/customer/', views.CustomerListView.as_view(), name='customer_list'),

    path('edit/session/<int:session_id>/', views.SessionEditView.as_view(), name='session_edit'),
    path('edit/customer/<int:customer_id>/', views.CustomerEditView.as_view(), name='customer_edit'),

    path('delete/location/<int:location_id>/', views.LocationDeleteView.as_view(), name='location_delete'),
    path('delete/session/<int:session_id>/', views.SessionDeleteView.as_view(), name='session_delete'),

    path('calculation/session/<int:session_id>/', views.SessionCalculationView.as_view(), name='session_calculation'),
]
