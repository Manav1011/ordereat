from django.contrib import admin
from .models import Outlet, Franchise, MenuCategory, MenuItem, Order, OrderItem

class ReadOnlySlugAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)

@admin.register(Outlet)
class OutletAdmin(ReadOnlySlugAdmin):
    pass

@admin.register(Franchise)
class FranchiseAdmin(ReadOnlySlugAdmin):
    pass

@admin.register(MenuCategory)
class MenuCategoryAdmin(ReadOnlySlugAdmin):
    pass

@admin.register(MenuItem)
class MenuItemAdmin(ReadOnlySlugAdmin):
    pass

@admin.register(Order)
class OrderAdmin(ReadOnlySlugAdmin):
    pass

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass