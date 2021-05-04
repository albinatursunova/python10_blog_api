from rest_framework import serializers

from main.models import Category, Tag, Post


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('title', 'image')

    def validate_title(self, title):
        if self.Meta.model.objects.filter(title=title).exists():
            raise serializers.ValidationError('Заголовок не может повторяться')
        return title


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('title', )

    def validate_title(self, title):
        if self.Meta.model.objects.filter(title=title).exists():
            raise serializers.ValidationError('Заголовок не может повторяться')
        return title

# serializers.Serializer - разница: в Model всё прописано
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('slug', )

# Form и ModelForm -> ModelForm(Form)
