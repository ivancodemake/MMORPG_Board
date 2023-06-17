from django.urls import path
from .views import BoardList, BoardCreate, BoardUpdate, BoardDetail, BoardAuthorList, BoardCategoryList, accept, delete


urlpatterns = [
    path('', BoardList.as_view(), name='boardlist'),
    path('create/', BoardCreate.as_view(), name='create'),
    path('<int:pk>/', BoardDetail.as_view(), name='detail'),
    path('edit/<int:pk>/', BoardUpdate.as_view(), name='edit'),
    path('myboard/<int:pk>/', BoardAuthorList.as_view(), name='myboard'),
    path('accept/<int:pk>/', accept, name='accept'),
    path('delete/<int:pk>/', delete, name='delete'),
    path('category/<int:pk>/', BoardCategoryList.as_view(), name='category'),
]
