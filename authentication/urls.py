from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
urlpatterns = [
    path('token/refresh/', view=TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', view=TokenObtainPairView.as_view(), name='token_obtain_pair'),

]
