# parking/resources.py
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from rest_api.models import ParkingDetail, VehicleDetail, Parking

class ParkingReportResource(resources.ModelResource):
    parking_wing = Field(
        column_name='parking_wing',
        attribute='parking_wing',
        widget=ForeignKeyWidget(Parking, 'wing_name')
    )
    vehicles = Field(
        column_name='vehicles',
        attribute='vehicles',
        widget=ManyToManyWidget(VehicleDetail, separator=',')
    )

    class Meta:
        model = ParkingDetail
        fields = ('id', 'parking_wing', 'vehicles', 'vehicle_arrived_date', 'vehicle_arrived_time', 'vehicle_left_date', 'vehicle_left_time', 'vehicle_has_left')
        import_id_fields = ('id',)
        
    def before_import_row(self, row, **kwargs):
        # You can modify the row here if needed
        pass

    def after_import_row(self, row, instance, **kwargs):
        # Called after each row is imported
        # You can add custom logic here if needed
        pass