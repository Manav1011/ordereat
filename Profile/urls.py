from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import CreateFranchiseAdminView, CreateOutletAdminView, SetPasswordView, UpdateProfileView

urlpatterns = [    
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('franchises/<slug:franchise_slug>/set-admin/', CreateFranchiseAdminView.as_view(), name='set-franchise-admin'),
    path('outlets/<slug:outlet_slug>/set-admin/', CreateOutletAdminView.as_view(), name='set-outlet-admin'),
    path('set-password/', SetPasswordView.as_view(), name='set-password'),
    path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),
]
