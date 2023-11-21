# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.urls import path

from blog import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("ResourceEase/resource_list/", views.PostListView.as_view(), name="resource_list"),
    path("ResourceEase/resource/<slug>/", views.PostDetailView.as_view(), name="resource_detail"),
    path("ResourceEase/search/", views.SearchView.as_view(), name="search"),
    path(
        "ResourceEase/contribute",
        login_required(views.ContributeView.as_view()),
        name="contribute",
    ),
        path(
        "ResourceEase/contribute/Create_a_new_Resource",
        login_required(views.PostCreateView.as_view()),
        name="resource_create",
    ),
    path(
        "ResourceEase/resource/update/<slug>/",
        login_required(views.PostUpdateView.as_view()),
        name="resource_update",
    ),

    path(
        "ResourceEase/resource/delete/<slug>/",
        login_required(views.PostDeleteView.as_view()),
        name="resource_delete",
    ),

    path(
        "ResoureEase/Contribute/upload/", 
         login_required(views.ResourceUploadPDFView.as_view()),
        name='upload_pdf'
    ),

  path('chatbot/', views.chatbot_ui, name='chatbot_ui'),
  path('get_bot_response/', views.get_bot_response, name='get_bot_response'),
]


