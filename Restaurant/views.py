from django.shortcuts import render
from rest_framework import generics, permissions, serializers

from .models import Franchise, Outlet, MenuCategory, MenuItem, Order, OrderItem
from django.db.models import Q
from .serializers import (
    FranchiseSerializer, OutletSerializer, MenuCategorySerializer,
    MenuItemWriteSerializer, MenuItemReadSerializer, OrderSerializer, OrderItemSerializer
)
from .permissions import IsOutletOrFranchiseAdmin, IsUserSuperuser, IsRestaurantAdmin, IsOutletAdmin
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema

# Franchise Views
class FranchiseListCreateView(generics.ListCreateAPIView):
    queryset = Franchise.objects.all()
    serializer_class = FranchiseSerializer
    permission_classes = [IsUserSuperuser]        

class FranchiseDetailView(generics.RetrieveDestroyAPIView):
    queryset = Franchise.objects.all()
    serializer_class = FranchiseSerializer
    permission_classes = [permissions.IsAuthenticated, IsRestaurantAdmin]
    lookup_field = "slug"

# Outlet Views
class OutletListCreateView(generics.ListCreateAPIView):    
    serializer_class = OutletSerializer
    permission_classes = [permissions.IsAuthenticated, IsRestaurantAdmin]
    
    def get_queryset(self):
        user = self.request.user
        return Outlet.objects.filter(franchise__admin=user)
        
class OutletDetailView(generics.RetrieveAPIView):
    serializer_class = OutletSerializer
    permission_classes = [permissions.IsAuthenticated, IsOutletOrFranchiseAdmin]
    lookup_field = "slug"

    def get_queryset(self):
        user = self.request.user        

        if user.is_anonymous or not user:
            return Outlet.objects.none()

        return Outlet.objects.filter(
            Q(admin=user) | Q(franchise__admin=user)
        )
    
# MenuCategory Views
class MenuCategoryListCreateView(generics.ListCreateAPIView):    
    serializer_class = MenuCategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOutletAdmin]
    
    def get_queryset(self):
        user = self.request.user        

        if user.is_anonymous or not user:
            return Outlet.objects.none()

        return MenuCategory.objects.filter(
            Q(outlet__admin=user)
        )
        

class MenuCategoryDetailView(generics.RetrieveDestroyAPIView):    
    serializer_class = MenuCategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOutletAdmin]
    lookup_field = "slug"

    def get_queryset(self):                
        user = self.request.user
        return MenuCategory.objects.filter(outlet__admin=user)

        
# MenuItem Views
@extend_schema(
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
                'category': {'type': 'string'},
                'description': {'type': 'string'},
                'price': {'type': 'number'},
                'image': {'type': 'string', 'format': 'binary'}
            }
        }
    }
)
class MenuItemListCreateView(generics.ListCreateAPIView):        
    permission_classes = [permissions.IsAuthenticated, IsOutletAdmin]    
    parser_classes = [MultiPartParser, FormParser]    
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MenuItemWriteSerializer
        return MenuItemReadSerializer

    def get_queryset(self):
        return MenuItem.objects.filter(category__outlet__admin=self.request.user)

class MenuItemDetailView(generics.RetrieveDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemReadSerializer
    permission_classes = [permissions.IsAuthenticated, IsOutletAdmin]
    lookup_field = "slug"