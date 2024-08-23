from django.contrib import admin
from rest_api.models import (
    CustomUser,
    Parking,
    ParkingDetail,
    VehicleDetail,
    VehicleOwner,
    Document,
    Comment
    
)
from import_export.admin import ImportExportModelAdmin
from rest_api.resources import ParkingReportResource
from modeltranslation.admin import TranslationAdmin


@admin.register(Parking)
class ParkingAdmin(TranslationAdmin):
    list_display = ('wing_name', 'is_available')


@admin.register(ParkingDetail)
class ReportAdmin(ImportExportModelAdmin):
    
     resource_class = ParkingReportResource   
     
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'file')
    search_fields = ('title',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'document', 'content', 'page', 'x1', 'y1', 'x2', 'y2', 'height', 'width')
    search_fields = ('content', 'document__title', 'user__username')
    list_filter = ('document', 'user', 'page')


admin.site.register(Document, DocumentAdmin)
admin.site.register(Comment, CommentAdmin)   
admin.site.register(VehicleDetail),
admin.site.register(CustomUser),
admin.site.register(VehicleOwner),
