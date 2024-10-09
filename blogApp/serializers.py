from rest_framework import serializers
from .models import Post
import json


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['page_name', 'page_title', 'side_panel', 'map_image', 'body_content', 'static_table', 'dynamic_table', 'slug']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.side_panel:
            representation['side_panel'] = json.loads(instance.side_panel)
        if instance.body_content:
            representation['body_content'] = json.loads(instance.body_content)
        if instance.static_table:
            representation['static_table'] = json.loads(instance.static_table)
        if instance.dynamic_table:
            representation['dynamic_table'] = json.loads(instance.dynamic_table)
        return representation