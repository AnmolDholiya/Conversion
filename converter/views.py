from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.conf import settings
from django.http import FileResponse, Http404
from .serializers import FileUploadSerializer, ImageConversionSerializer
from .utils import convert_image, convert_to_pdf, convert_to_word, merge_images_to_pdf, compress_image, compress_pdf
from .models import ImageConversion
import os

class DownloadFileView(APIView):
    """
    View to force download of a file using Content-Disposition header.
    """
    def get(self, request):
        file_path = request.query_params.get('path')
        if not file_path:
            return Response({"error": "Path parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Security: Prevent directory traversal
        if '..' in file_path or file_path.startswith('/') or file_path.startswith('\\'):
            return Response({"error": "Invalid path"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Normalize slashes for the current OS
        normalized_path = file_path.replace('/', os.path.sep).replace('\\', os.path.sep)
        full_path = os.path.join(settings.MEDIA_ROOT, normalized_path)
        if not os.path.exists(full_path):
            raise Http404("File not found")
            
        response = FileResponse(open(full_path, 'rb'), as_attachment=True)
        # Extract filename for the attachment header
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(full_path)}"'
        return response

class BaseConversionView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def get_serializer(self, *args, **kwargs):
        return FileUploadSerializer(*args, **kwargs)

    def handle_exception(self, exc):
        return Response(
            {"error": str(exc)},
            status=status.HTTP_400_BAD_REQUEST
        )

class ConvertImageFormatView(BaseConversionView):
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']
            target_format = serializer.validated_data.get('target_format', 'JPG').upper()
            
            if target_format not in ['JPG', 'JPEG', 'PNG']:
                return Response({"error": "Unsupported target format. Use JPG or PNG."}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                # Create model instance
                conversion = ImageConversion.objects.create(
                    original_file=uploaded_file,
                    conversion_type='FORMAT',
                    target_format=target_format
                )
                
                # Perform conversion
                relative_path = convert_image(uploaded_file, target_format)
                
                # Update model instance
                conversion.converted_file = relative_path
                conversion.save()
                
                return Response({
                    "message": "Image converted successfully",
                    "converted_url": request.build_absolute_uri(settings.MEDIA_URL + relative_path)
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConvertToPDFView(BaseConversionView):
    def post(self, request):
        uploaded_files = request.FILES.getlist('file')
        merge = request.data.get('merge', 'false').lower() == 'true'

        if not uploaded_files:
            return Response({"error": "No files provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if merge and len(uploaded_files) > 1:
                # Merge all images into a single multi-page PDF
                relative_path = merge_images_to_pdf(uploaded_files)
                if not relative_path:
                    return Response({"error": "Failed to merge images into PDF."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response({
                    "message": f"Merged {len(uploaded_files)} images into PDF successfully",
                    "converted_url": request.build_absolute_uri(settings.MEDIA_URL + relative_path)
                }, status=status.HTTP_200_OK)
            else:
                # Single file conversion
                uploaded_file = uploaded_files[0]
                conversion = ImageConversion.objects.create(
                    original_file=uploaded_file,
                    conversion_type='PDF',
                    target_format='PDF'
                )
                relative_path = convert_to_pdf(uploaded_file)
                conversion.converted_file = relative_path
                conversion.save()
                return Response({
                    "message": "Converted to PDF successfully",
                    "converted_url": request.build_absolute_uri(settings.MEDIA_URL + relative_path)
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CompressImageView(BaseConversionView):
    def post(self, request):
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quality = int(request.data.get('quality', 60))
            quality = max(1, min(95, quality))  # clamp to valid range
        except (ValueError, TypeError):
            quality = 60

        try:
            relative_path, original_size, compressed_size = compress_image(uploaded_file, quality)
            saved_bytes = original_size - compressed_size
            saved_percent = round((saved_bytes / original_size) * 100, 1) if original_size > 0 else 0

            return Response({
                "message": "Image compressed successfully",
                "converted_url": request.build_absolute_uri(settings.MEDIA_URL + relative_path),
                "original_size": original_size,
                "compressed_size": compressed_size,
                "saved_percent": saved_percent,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConvertToWordView(BaseConversionView):
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']
            
            try:
                conversion = ImageConversion.objects.create(
                    original_file=uploaded_file,
                    conversion_type='WORD',
                    target_format='DOCX'
                )
                
                relative_path = convert_to_word(uploaded_file)
                
                conversion.converted_file = relative_path
                conversion.save()
                
                return Response({
                    "message": "Converted to Word successfully",
                    "converted_url": request.build_absolute_uri(settings.MEDIA_URL + relative_path)
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CompressPDFView(BaseConversionView):
    def post(self, request):
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if file is PDF
        if not uploaded_file.name.lower().endswith('.pdf'):
            return Response({"error": "Only PDF files are supported for this feature."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quality = int(request.data.get('quality', 60))
            quality = max(1, min(95, quality))
        except (ValueError, TypeError):
            quality = 60

        try:
            relative_path, original_size, compressed_size = compress_pdf(uploaded_file, quality)
            saved_bytes = original_size - compressed_size
            saved_percent = round((saved_bytes / original_size) * 100, 1) if original_size > 0 else 0

            return Response({
                "message": "PDF compressed successfully",
                "converted_url": request.build_absolute_uri(settings.MEDIA_URL + relative_path),
                "original_size": original_size,
                "compressed_size": compressed_size,
                "saved_percent": max(0, saved_percent), # No negative savings reported
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
