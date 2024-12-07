from django.urls import path
from . import views
from .views import (
    ProductInfoListView, ProductInfoCreateView, ProductInfoUpdateView,
    ProductInfoDeleteView, ProductInfoTempListView, SSOListView, MFAListView
)

urlpatterns = [
    path('', ProductInfoListView.as_view(), name='product_list'),
    path('sso/', SSOListView.as_view(), name='sso_list'),
    path('mfa/', MFAListView.as_view(), name='mfa_list'),
    path('new/', ProductInfoCreateView.as_view(), name='product_create'),
    path('<int:pk>/edit/', ProductInfoUpdateView.as_view(), name='product_edit'),
    path('<int:pk>/delete/', ProductInfoDeleteView.as_view(), name='product_delete'),
    path('temp/', ProductInfoTempListView.as_view(), name='temp_product_list'),
    path('update_sso/<int:product_id>/', views.update_sso, name='update_sso'),
    path('review_sso/<int:temp_id>/', views.review_sso, name='review_sso'),
    path('notifications/', views.notifications, name='notifications'),
]
