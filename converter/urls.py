from django.urls import path
from .views import ConvertImageFormatView, ConvertToPDFView, ConvertToWordView, DownloadFileView, CompressImageView, CompressPDFView

urlpatterns = [
    path('convert-image-format/', ConvertImageFormatView.as_view(), name='convert-image-format'),
    path('convert-to-pdf/', ConvertToPDFView.as_view(), name='convert-to-pdf'),
    path('convert-to-word/', ConvertToWordView.as_view(), name='convert-to-word'),
    path('compress-image/', CompressImageView.as_view(), name='compress-image'),
    path('compress-pdf/', CompressPDFView.as_view(), name='compress-pdf'),
    path('download/', DownloadFileView.as_view(), name='download-file'),
]
