import logging
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_api.filters import ParkingDetailFilter
from rest_api.models import Parking, ParkingDetail, VehicleDetail, Document, Comment
from rest_api.pagination import *
from rest_api.permissions import IsAdminUser, IsEmployee, IsOwner
from rest_api.serializers import (
    ParkingDetailSerializer,
    ParkingSerializer,
    VehicleDetailSerializer,
    ParkingReportSerializer,
    CommentSerializer,
    DocumentSerializer
)
from rest_api.tasks import send_registration_email
from rest_framework import generics, viewsets
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from rest_api.resources import ParkingReportResource
from rest_framework.decorators import api_view, permission_classes
from import_export.formats.base_formats import CSV
from django.http import HttpResponse
from datetime import datetime
import csv
import io
from rest_framework.response import Response
from io import StringIO
from rest_framework import status
from rest_framework.views import APIView
from django.utils.translation import activate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from rest_api.pdf_utils import extract_text_and_images, add_comment_to_pdf, find_bbox_for_coordinates
from rest_framework import viewsets, status
from rest_framework.response import Response
import fitz 
# Create your views here.
# Generics API
class ParkingCreateAPIView(generics.CreateAPIView):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer

    def perform_create(self, serializer):
        request = self.request
        lang_code = request.LANGUAGE_CODE if request else 'en'

        # Prepare data for translation fields
        data = request.data
        if lang_code == 'ne':
            wing_name_field = 'wing_name_ne'
        else:
            wing_name_field = 'wing_name_en'

        # Pass data directly to serializer
        serializer.save(**{wing_name_field: data.get(wing_name_field, '')})
class ParkingUpdateAPIView(UpdateAPIView):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class ParkingListAPIView(ListAPIView, PageNumberPagination):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsEmployee]
    pagination_class = CustomCursorPagination
    
    def get_queryset(self):
        lang_code = self.request.LANGUAGE_CODE if self.request.LANGUAGE_CODE else 'en'
        activate(lang_code)
        return super().get_queryset()


class ParkingDestroyAPIView(DestroyAPIView):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class ParkingRetrieveAPIView(RetrieveAPIView):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    permission_classes = [IsAuthenticated]


# Parking Detail View for Employees
class ParkingDetailCreateAPIView(CreateAPIView):
    queryset = ParkingDetail.objects.all()
    serializer_class = ParkingDetailSerializer
    permission_classes = [IsAuthenticated, IsEmployee, IsAdminUser]
    pagination_class = CustomLimitOffsetPagination


# Viewset
# @method_decorator(csrf_exempt, name='dispatch')


class VehicleDetailViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleDetailSerializer
    # permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]
    pagination_class = CustomLimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        return VehicleDetail.objects.filter(owner__user=user)


class NoPagination(PageNumberPagination):
    page_size = 1000


class ParkingDetailViewSet(viewsets.ModelViewSet):
    serializer_class = ParkingDetailSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsAdminUser | IsEmployee]
    pagination_class = NoPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ParkingDetailFilter

    def get_queryset(self):
        # Ensure the authenticated user has a VehicleOwner instance associated
        user = self.request.user
        if user.is_superuser:
            return ParkingDetail.objects.all()
        elif hasattr(user, "vehicle_owner"):
            # Filter parking details based on the owner's vehicles
            return ParkingDetail.objects.filter(vehicles__owner=user.vehicle_owner)
        else:
            # Handle case where user does not have a VehicleOwner instance
            return ParkingDetail.objects.none()


User = get_user_model()
logger = logging.getLogger(__name__)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ExportParkingReport(request):
    """
    Exports the parking details of vehicles associated with the authenticated user to a CSV file.

    Retrieves all parking details where the vehicle's owner is the authenticated user.
    Writes these details into a CSV format and sends the file as an HTTP response.

    Args:
        request (HttpRequest): The request object containing user details.

    Returns:
        HttpResponse: An HTTP response with the CSV file containing parking details.
    """
    user = request.user
    parking_details = ParkingDetail.objects.filter(
        vehicles__owner__user=user
    ).distinct()


    for detail in parking_details:
        print(f"Parking Detail: {detail}")
        for vehicle in detail.vehicles.all():
            print(f"Vehicle: {vehicle}, Owner: {vehicle.owner}")

    if not parking_details:
        return HttpResponse("No parking details found for this user.", status=404)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Parking Wing', 'Vehicle Number', 'Owner Name', 'Arrived Date', 'Arrived Time', 'Left Date', 'Left Time', 'Has Left'])
    print("CSV Header written.")

    for detail in parking_details:
        for vehicle in detail.vehicles.all():
            writer.writerow([
                detail.parking_wing or "N/A",
                vehicle.vehicle_number or "N/A",
                vehicle.owner.name if vehicle.owner else "Unknown Owner",
                detail.vehicle_arrived_date,
                detail.vehicle_arrived_time,
                detail.vehicle_left_date or "N/A",
                detail.vehicle_left_time or "N/A",
                detail.vehicle_has_left
            ])
    csv_content = output.getvalue()
    print(f"CSV Content:\n{csv_content}")
    
    # Create HTTP response with the CSV data
    response = HttpResponse(csv_content, content_type='text/csv')
    now = datetime.now().strftime('%Y%m%d_%H%M%S') 
    filename = f"parking_reports_{now}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    output.seek(0)
    output.close()
    print("CSV file generated and response prepared.")

    return response






class ImportParkingReport(APIView):
    """
    Imports parking details from a CSV file and stores them in the database.

    Reads a CSV file containing parking details, parses it, and creates or updates
    ParkingDetail instances based on the data.

    Args:
        request (HttpRequest): The request object containing the CSV file.

    Returns:
        Response: A response indicating the success or failure of the import process.
    """
    def post(self, request, *args, **kwargs):
        serializer = ParkingReportSerializer(data=request.data)
        if serializer.is_valid():
            csv_file = serializer.validated_data.get('file')
            if csv_file is None:
                return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

            if not csv_file.name.endswith('.csv'):
                return Response({'error': 'File is not CSV type'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Read CSV file
                data = csv_file.read().decode('utf-8')
                io_string = StringIO(data)
                reader = csv.DictReader(io_string)

                for row in reader:
                    parking_wing_id = row.get('parking_wing')
                    vehicles_ids = row.get('vehicles', '').split(',')
                    vehicle_arrived_date = row.get('vehicle_arrived_date')
                    
                    vehicle_arrived_time_str = row.get('vehicle_arrived_time', '')
                    vehicle_left_date = row.get('vehicle_left_date', '')
                    vehicle_left_time_str = row.get('vehicle_left_time', '')
                    vehicle_has_left_str = row.get('vehicle_has_left', 'False')
                    
                    
                    try:
                        vehicle_arrived_time = datetime.strptime(vehicle_arrived_time_str, '%H:%M:%S').time() if vehicle_arrived_time_str else None
                    except ValueError as e:
                        vehicle_arrived_time = None
                    
                    try:
                        vehicle_left_time = datetime.strptime(vehicle_left_time_str, '%H:%M:%S').time() if vehicle_left_time_str else None
                    except ValueError as e:
                        vehicle_left_time = None
                    
                    vehicle_has_left = vehicle_has_left_str.strip().lower() in ['true', '1', 't', 'y', 'yes']

                    if not parking_wing_id:
                        return Response({'error': 'Parking wing ID is missing'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    try:
                        parking_wing = Parking.objects.get(id=parking_wing_id)
                    except Parking.DoesNotExist:
                        return Response({'error': f'Parking wing with ID {parking_wing_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    vehicles = VehicleDetail.objects.filter(id__in=vehicles_ids)

                    # Create or update ParkingDetail instance
                    parking_detail = ParkingDetail.objects.create(
                        parking_wing=parking_wing,
                        vehicle_arrived_date=vehicle_arrived_date,
                        vehicle_arrived_time=vehicle_arrived_time,
                        vehicle_left_date=vehicle_left_date if vehicle_left_date else None,
                        vehicle_left_time=vehicle_left_time if vehicle_left_time else None,
                        vehicle_has_left=vehicle_has_left
                    )

                    # Set the many-to-many relationship
                    parking_detail.vehicles.set(vehicles)

                return Response({'message': 'CSV file processed successfully'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    
class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = (MultiPartParser, FormParser)

    @action(detail=True, methods=['post'], url_path='annotate', parser_classes=[JSONParser])
    def annotate_pdf(self, request, pk=None):
        try:
            document = self.get_object()
        except Document.DoesNotExist:
            return Response({"detail": "No Document matches the given query."}, status=status.HTTP_404_NOT_FOUND)

        comments_data = request.data.get('comments')
        pdf_path = document.file.path
        doc = fitz.open(pdf_path)
        num_pages = len(doc)

        for comment in comments_data:
            if comment['page'] >= num_pages:
                return Response({"detail": f"Page {comment['page']} not in document"}, status=status.HTTP_400_BAD_REQUEST)
            comment['document'] = document.id

        comments = CommentSerializer(data=comments_data, many=True)

        if comments.is_valid():
            comments.save()

            comments_for_annotation = []
            for comment in comments_data:
                page = comment["page"]
                content = comment["content"]
                if comment.get("whole_page", False):
                    bbox = (0, 0, doc.load_page(page).rect.width, doc.load_page(page).rect.height)
                else:
                    bbox = (comment["x1"], comment["y1"], comment["x2"], comment["y2"])
                comments_for_annotation.append({
                    "page": page,
                    "bbox": bbox,
                    "text": content
                })

            output_path = pdf_path.replace('.pdf', '_annotated.pdf')
            add_comment_to_pdf(pdf_path, output_path, comments_for_annotation)

            return Response({"status": "success", "message": "PDF annotated successfully"}, status=status.HTTP_200_OK)
        return Response(comments.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='comments')
    def get_comments(self, request, pk=None):
        document = self.get_object()
        comments = Comment.objects.filter(document=document)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer