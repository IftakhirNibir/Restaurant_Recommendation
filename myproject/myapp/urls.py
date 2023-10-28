from django.urls import path
from .views import *

urlpatterns = [
    path("",homepage,name="homepage"),
    path("trending",trending,name="trending"),
    path("recommendation", recommendation_page, name="recommendation_part1"),
    path("recommendation2/<str:restu>/", recommendation2_page, name="recommendation_part_two"),
    path('cluster', Cluster, name="cluster"),
]