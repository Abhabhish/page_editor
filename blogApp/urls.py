from . import views
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    path('', views.sections, name="sections-page"),
    path(r'posts/<int:sid>', views.posts, name="posts-page"),
    path('login',auth_views.LoginView.as_view(template_name="login.html",redirect_authenticated_user = True),name='login'),
    path('userlogin', views.login_user, name="login-user"),
    path('user-register', views.registerUser, name="register-user"),
    path('logout',views.logoutuser,name='logout'),
    path('profile',views.profile,name='profile'),
    path('update-profile',views.update_profile,name='update-profile'),
    path('update-avatar',views.update_avatar,name='update-avatar'),
    path('category_mgt',views.category_mgt,name='category-mgt'),
    path('manage_category',views.manage_category,name='manage-category'),
    path(r'manage_category/<int:pk>',views.manage_category,name='edit-category'),
    path('save_category',views.save_category,name='save-category'),
    path('delete_category',views.delete_category,name='delete-category'),
    path('post_mgt',views.post_mgt,name='post-mgt'),
    path(r'edit_post/<str:lang>/<int:pk>',views.edit_post,name='edit-post'),
    path(r'edit_post/<str:lang>/<int:pk>/<str:tr>',views.edit_post,name='edit-post'),
    path(r'edit_section/<int:pk>',views.edit_section,name='edit-section'),
    path(r'edit_folder/<int:pk>',views.edit_folder,name='edit-folder'),
    path('save_post',views.save_post,name='save-post'),
    path('save_section',views.save_section,name='save-section'),
    path('add_post',views.add_post,name='add-post'),
    path('add_section',views.add_section,name='add-section'),
    path(r'delete_post/<int:pk>',views.delete_post,name='delete-post'),
    path(r'delete_section/<int:pk>',views.delete_section,name='delete-section'),
    path(r'delete_folder/<int:pk>',views.delete_folder,name='delete-folder'),
    path(r'view_post/<int:pk>',views.view_post,name='view-post'),
    path(r'<int:pk>',views.post_by_category,name='category-post'),
    path('categories',views.categories,name='category-page'),
    path(r'edit_folder/<int:folder_id>',views.categories,name='edit-folder'),
    path(r'delete_folder/<int:folder_id>',views.categories,name='delete-folder'),





    path('section/<int:section_id>/create-folder/', views.create_folder, name='create_folder_in_section'),
    path('section/<int:section_id>/create-folder/<int:parent_folder_id>/', views.create_folder, name='create_subfolder'),

    path('folder/<int:folder_id>/create-post/', views.create_post, name='create_post'),
    
    path('folder/<int:folder_id>/', views.folder_view, name='folder_view'),
    path('section/<int:section_id>/', views.section_view, name='section_view'),
]
