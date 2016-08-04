from django.contrib import admin

# Register your models here.

from .models import (
    Categories,
    Products,
    Orders,
    OrderProducts,
    Buyers
    # Users,
)

admin.ModelAdmin.actions_on_bottom = True


# class UsersAdmin(admin.ModelAdmin):
#     list_display = ['id', 'phone', ]
#     fields = ['username']


# своя панелька справа
class BlaListFilter(admin.SimpleListFilter):
    title = 'My Filter'
    parameter_name = 'bla'

    def lookups(self, request, model_admin):
        # return [('100-200', '100-200'), ('200-300', '200-300'), ]
        qs = model_admin.get_queryset(request)
        if qs.filter(price__gte=100, price__lte=200).exists():  # наличие в списке записей
            yield ('100-200', '100-200')

    def queryset(self, request, queryset):
        if self.value == '100-200':
            return queryset.filter(price__gte=100, price__lte=200)



class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    # list_display_links = ['name']
    list_editable = ['name']
    list_per_page = 10
    fields = ['name']
    search_fields = ['name']


class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'image', ]
    list_per_page = 10
    list_display_links = ['id', 'name']
    list_editable = ['category']
    list_filter = ['category']
    search_fields = ['name', 'price']
    fieldsets = (
        (
            None,
            {
                'fields': (
                    ('name', 'price'),
                    'quantity',
                    'category',
                    'image')
            }
        ),
        (
            'Advanced options',
            {
                'classes': ('wide', ),
                'fields': (
                    ('size', 'colour'),
                    'description',
                ),
                'description': 'Advanced fields',
            }
        )
    )
    show_full_result_count = False


class OrderProductsInLine(admin.TabularInline):
    model = OrderProducts
    extra = 1


class OrdersAdmin(admin.ModelAdmin):
    inlines = (OrderProductsInLine,)
    list_display = ['id', 'user', 'total_sum', 'date', ]
    list_display_links = ['date', ]
    list_editable = ('user',)
    list_filter = ('date',)
    search_fields = ('total_sum',)
    date_hierarchy = 'date'
    show_full_result_count = False

    # mode

    # class Media:
    #     css = {
    #         "all": ('my_style.css', )
    #     }
    #     js = ('my_code.js', )


class OrdersProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'sum', ]
    list_display_links = ['id', 'order', ]
    list_editable = ['product', 'quantity', 'sum']
    show_full_result_count = False


class BuyersAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone']


admin.site.register(Buyers, BuyersAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrderProducts, OrdersProductsAdmin)
