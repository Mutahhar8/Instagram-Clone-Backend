from django.urls import path
from .views import SignupView, LoginView, LogoutView, ShowDataView, UserInformationUpdateView, SearchAllProfiles

urlpatterns = [
    path('signup/', view = SignupView.as_view(), name = 'sign_up'),
    path('login/', view = LoginView.as_view(), name = 'login_view'),
    path('logout/', view = LogoutView.as_view(), name='logout_view'),
    path('showdata/', view= ShowDataView.as_view(), name='show_data' ),
    path('search_profile/<str:search_term>/', view= SearchAllProfiles.as_view(), name='search_profile'),
    path('update_details/', view= UserInformationUpdateView.as_view(), name='update_details'),
]