from django.urls import path
from . import views

urlpatterns = [
    # Franchise
    path('franchises/', views.FranchiseListCreateView.as_view(), name='franchise-list-create'),
    path('franchises/<slug:slug>/', views.FranchiseDetailView.as_view(), name='franchise-detail'),

    # Outlet
    path('outlets/', views.OutletListCreateView.as_view(), name='outlet-list-create'),
    path('outlets/<slug:slug>/', views.OutletDetailView.as_view(), name='outlet-detail'),

    # MenuCategory
    path('categories/', views.MenuCategoryListCreateView.as_view(), name='menucategory-list-create'),
    path('categories/<slug:slug>/', views.MenuCategoryDetailView.as_view(), name='menucategory-detail'),

    # MenuItem
    path('menu-items/', views.MenuItemListCreateView.as_view(), name='menuitem-list-create'),
    path('menu-items/<slug:slug>/', views.MenuItemDetailView.as_view(), name='menuitem-detail')
]