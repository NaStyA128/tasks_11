from django.contrib import admin

# Register your models here.

from .models import (
    Categories,
    Products,
    Orders,
    OrderProducts,
)


# admin.site.register(Categories)
# admin.site.register(Products)


# @admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    pass


class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'image', ]
    fields = ['name', 'price', 'category', 'image', ]
    actions = []
    actions_on_bottom = True
    # empty_value_display = 'Empty'


class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id', 'total_sum', 'date', 'user', ]
    # fields = ['products', ]
    date_hierarchy = 'date'
    list_display_links = ('id', 'date')
    list_editable = ('user', )
    list_filter = ('date', )
    search_fields = ('total_sum', )
    actions = ['show_data', ]

    def show_data(self, obj):
        return 'hi'
    show_data.short_description = 'update to today'


class OrdersProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'order', 'quantity', 'sum', ]
    # fields = ['product', 'order', 'quantity', 'sum', ]
    fieldsets = ((None,
                 {
                     'fields': (('product', 'order', ), 'quantity', 'sum')
                 }
                 ),
                 (
                     'Advanced options', {
                         'classes': ('collapse', ),  # wide
                         'fields': ('quantity', ),
                         'description': '<b>This is description</b>',
                     }
                 ),)
    # fieldsets =
    # date_hierarchy = 'date'


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrderProducts, OrdersProductsAdmin)
