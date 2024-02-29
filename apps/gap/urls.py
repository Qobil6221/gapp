from django.urls import path

from apps.gap.views import RoomListView, RoomDetailView, LikeOpinionView, SearchOpinionView, OpinionDetailView, \
    Loginview, UserRegisterView, UserLogoutView, AddOpinionView, delete_opinion

app_name = 'gap'
urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='rooms'),
    path('room/<pk>', RoomDetailView.as_view(), name='room'),
    path('opinion/<int:pk>', OpinionDetailView.as_view(), name='opinion'),
    path('like/<pk>', LikeOpinionView.as_view(), name='opinion-like'),
    path('search', SearchOpinionView.as_view(), name='search-opinion'),
    path('login/', Loginview.as_view(), name='login-page'),
    path('register/', UserRegisterView.as_view(), name='register-page'),
    path('logout/', UserLogoutView.as_view(), name="logout"),
    path('add/', AddOpinionView.as_view(), name="add-opinion"),
    path('delete/<id>', delete_opinion, name="delete-opinion"),

]
