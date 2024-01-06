from django.urls import path
from templates.views import (
    PostDetail, PostCreate, PostEdit, PostDelete,
    CategoryList, PostOfCategoryList, subscribe_to_category)

urlpatterns = [
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='delete'),
    path('category/', CategoryList.as_view(), name='categories'),
    path('category/<int:pk>/', PostOfCategoryList.as_view(),
         name='posts_of_categories_list'),
    path('category/<int:pk>/subscribe', subscribe_to_category,
         name='subscribe_to_category'),

    ]
