from django.db import models
import os

class ImageConversion(models.Model):
    CONVERSION_TYPES = (
        ('FORMAT', 'Format Conversion'),
        ('PDF', 'Convert to PDF'),
        ('WORD', 'Convert to Word'),
    )
    
    original_file = models.FileField(upload_to='uploads/')
    converted_file = models.FileField(upload_to='conversions/', null=True, blank=True)
    conversion_type = models.CharField(max_length=10, choices=CONVERSION_TYPES)
    target_format = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.conversion_type} - {os.path.basename(self.original_file.name)}"
