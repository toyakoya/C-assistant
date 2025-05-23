from django.urls import path
from .views import ChatView, LocalSolveView, OnlineSolveView, LocalChatView, OnlineChatView,GetProblemView
urlpatterns = [
    path("models/", ChatView.as_view(), name="models"),
    path("localsolve/", LocalSolveView.as_view(), name="localsolve"), 
    path("onlinesolve/", OnlineSolveView.as_view(), name="onlinesolve"),
    path("localchat/", LocalChatView.as_view(), name="localchat"),
    path("onlinechat/", OnlineChatView.as_view(), name="onlinechat"),
    path("getproblem/", GetProblemView.as_view(), name="getproblem"),
]