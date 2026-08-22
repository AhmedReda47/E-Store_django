from rest_framework import serializers

from .models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    get_image = serializers.SerializerMethodField()
    get_thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "description",
            "price",
            "get_image",
            "get_thumbnail",
        )

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return ""

    def get_thumbnail(self, obj):
        if obj.thumbnail:
            return obj.thumbnail.url

        return ""

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "products",
        )