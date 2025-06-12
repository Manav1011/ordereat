from rest_framework import serializers
from .models import Franchise, Outlet, MenuCategory, MenuItem, Order, OrderItem

class FranchiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Franchise
        fields = ['name']

class OutletSerializer(serializers.ModelSerializer):    
    franchise = serializers.SlugField(write_only=True)
    class Meta:
        model = Outlet
        fields = ['name', 'franchise','slug']
        read_only_fields = ['slug']
        
    def validate(self, attrs):        
        franchise_slug = attrs.get('franchise')
        franchise_obj = Franchise.objects.filter(slug=franchise_slug).first()        
        if franchise_obj and franchise_obj.admin != self.context['request'].user:
            raise serializers.ValidationError("You do not have permission to create an outlet for this franchise.")
        if len(attrs.get('franchise', '')) == 0 or not franchise_obj:
            raise serializers.ValidationError("Franchise does not exist.")
        if len(attrs.get('name', '')) == 0:
            raise serializers.ValidationError("Name cannot be empty.")
        attrs['franchise_obj'] = franchise_obj
        return attrs

    def create(self, validated_data):
        franchise_obj = validated_data.pop('franchise_obj')
        # create an outlet obj:
        outlet_obj = Outlet.objects.get_or_create(
            name=validated_data.pop('name'), 
            franchise=franchise_obj
        )[0]
        return outlet_obj
    
class MenuCategorySerializer(serializers.ModelSerializer):
    outlet = serializers.SlugField(write_only=True)
    class Meta:
        model = MenuCategory
        fields = ["name","outlet","description","is_active","slug"]
        read_only_fields = ['slug',"is_active"]
    
    def validate(self, attrs):
        outlet_slug = attrs.get('outlet')
        outlet_obj = Outlet.objects.filter(slug=outlet_slug).first()        
        if outlet_obj.admin != self.context['request'].user:
            raise serializers.ValidationError("You do not have permission to create a menu category for this outlet.")
        if len(attrs.get('outlet', '')) == 0 or not outlet_obj:
            raise serializers.ValidationError("Outlet does not exist.")
        if len(attrs.get('name', '')) == 0:
            raise serializers.ValidationError("Name cannot be empty.")
        attrs['outlet_obj'] = outlet_obj
        return attrs
    
    def create(self, validated_data):
        outlet_obj = validated_data.pop('outlet_obj')
        # create a menu category obj:
        menu_category_obj = MenuCategory.objects.get_or_create(
            name=validated_data.pop('name'), 
            outlet=outlet_obj,
            description=validated_data.pop('description', ''),
            is_active=validated_data.pop('is_active', True)
        )[0]
        return menu_category_obj

class MenuItemWriteSerializer(serializers.ModelSerializer):
    category  = serializers.SlugField()
    image = serializers.ImageField(required=False, use_url=True)
    
    class Meta:
        model = MenuItem
        fields = ["name","category","description","price","is_available","image","slug"]
        read_only_fields = ['slug',"is_available"]
    
    def validate(self, attrs):        
        category_slug = attrs.get('category')
        category_obj = MenuCategory.objects.filter(slug=category_slug).first()        
        if category_obj.outlet.admin != self.context['request'].user:
            raise serializers.ValidationError("You do not have permission to create a menu item for this category.")
        if len(attrs.get('category', '')) == 0 or not category_obj:
            raise serializers.ValidationError("Menu Category does not exist.")
        if len(attrs.get('name', '')) == 0:
            raise serializers.ValidationError("Name cannot be empty.")
        attrs['category_obj'] = category_obj
        return attrs
    
    def create(self, validated_data):
        category_obj = validated_data.pop('category_obj')
        # create a menu item obj:
        menu_item_obj = MenuItem.objects.get_or_create(
            name=validated_data.pop('name'), 
            category=category_obj,
            description=validated_data.pop('description', ''),
            price=validated_data.pop('price', 0.0), 
            is_available=validated_data.pop('is_available', True),
            image=validated_data.pop('image', None)
        )[0]
        return menu_item_obj

class MenuItemReadSerializer(serializers.ModelSerializer):
    category = MenuCategorySerializer(read_only=True)
    image = serializers.ImageField(required=False, use_url=True)

    class Meta:
        model = MenuItem
        fields = ["name", "category", "description", "price", "is_available", "image", "slug"]    
        

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'