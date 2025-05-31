from PIL import Image

from django.apps import apps
from django.core.validators import ValidationError

def validate_image_size(image):
    file_size = image.size
    limit_mb = 5
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(f"The file size must not exceed {limit_mb}MB.")

def validate_image_dimensions(image):
    img = Image.open(image)
    min_width, min_height = 300, 300
    max_width, max_height = 4000, 4000

    width, height = img.size

    if width < min_width or height < min_height:
        raise ValidationError(f"The image is too small. Minimum size is {min_width}x{min_height} pixels.")

    if width > max_width or height > max_height:
        raise ValidationError(f"The image is too large. Maximum size is {max_width}x{max_height} pixels.")

def validate_image_count(product_id):
    ProductImage = apps.get_model('products', 'ProductImage') 
    max_images = 5
    if ProductImage.objects.filter(product_id=product_id).count() >= max_images:
        raise ValidationError(f"The product already has the maximum number of images ({max_images}).")
