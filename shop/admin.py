from django.contrib import admin

# Register your models here.

from .models import (
    Categories,
    Products,
    Orders,
    OrderProducts,
    MyUsers
)

admin.ModelAdmin.actions_on_bottom = True


class MyUsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'phone', ]
    search_fields = ['phone']


# своя панелька справа
class TotalSumListFilter(admin.SimpleListFilter):
    title = 'Total Sum'
    parameter_name = 'by total_sum'

    def lookups(self, request, model_admin):
        # return [('100-200', '100-200'), ('200-300', '200-300'), ]
        qs = model_admin.get_queryset(request)
        if qs.filter(total_sum__lte=200).exists():  # наличие в списке записей
            yield ('-200', '-200')
        if qs.filter(total_sum__gte=201, total_sum__lte=300).exists():
            yield ('201-300', '201-300')
        if qs.filter(total_sum__gte=301, total_sum__lte=500).exists():
            yield ('301-500', '301-500')
        if qs.filter(total_sum__gte=501).exists():
            yield ('501-', '501-')

    def queryset(self, request, queryset):
        if self.value() == '-200':
            return queryset.filter(total_sum__lte=200)
        elif self.value() == '201-300':
            return queryset.filter(total_sum__gte=201, total_sum__lte=300)
        elif self.value() == '301-500':
            return queryset.filter(total_sum__gte=301, total_sum__lte=500)
        elif self.value() == '501-':
            return queryset.filter(total_sum__gte=501)


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
    list_filter = ('date', TotalSumListFilter, )
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


# class BuyersAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'phone']


admin.site.register(MyUsers, MyUsersAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrderProducts, OrdersProductsAdmin)
