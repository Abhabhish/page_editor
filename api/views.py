import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from blogApp.models import Post
from rest_framework import generics
from blogApp.serializers import PostSerializer


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

post_detail_view = PostDetailAPIView.as_view()



