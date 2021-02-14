from rest_framework_json_api import serializers
from .models import Message, User, Follower

class UserSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.CharField(source='username')
    class Meta:
        model = User
        fields = ('user', )

class FollowSerializer(serializers.HyperlinkedModelSerializer):

    target_user = UserSerializer()

    class Meta:
        model = Follower
        fields = ('target_user', )

class MessageSerializer(serializers.HyperlinkedModelSerializer):

    author = UserSerializer()
    pub_date = serializers.CharField(source='publication_date')

    class Meta:
        model = Message
        fields = ('content', 'pub_date', 'author')

    def to_representation(self, instance):
        data = super(MessageSerializer, self).to_representation(instance)
        author = data.pop('author')
        for key, val in author.items():
            data.update({key: val})
        return data
