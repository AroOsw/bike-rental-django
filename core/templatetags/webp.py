# import os
# import logging
#
# from PIL import Image
#
# from django.conf import settings
# from django import template
#
# logger = logging.getLogger(__name__)
#
# register = template.Library()
#
# def convert_to_webp(image_path):
#     """
#     Converts an image to WebP format if it is not already in that format.
#     Returns the path to the converted image.
#     """
#     webp_path = os.path.splitext(image_path)[0] + '.webp'
#     print("webp path", webp_path)
#     print("image_path (input to be opened):", image_path)
#     open_img = Image.open(image_path)
#     logger.debug(f"Image opened: {open_img}")
#
#     # if not os.path.exists(webp_path):
#     #     try:
#     #         img = Image.open(image_path)
#     #         img.save(webp_path, 'WEBP', quality=80)
#     #         logger.debug(f"Converted {image_path} to WebP")
#     #     except Exception as e:
#     #         logger.error(f"Error converting image {image_path} to WebP: {e}")
#
#
# @register.simple_tag(takes_context=True)
# def webp(context, img_url):
#     """
#     Returns the URL of the WebP image if available, otherwise returns the original image URL.
#     """
#     static_path = settings.STATIC_URL + img_url
#     print("Image URL", img_url)
#     print("STATIC PATH", static_path)
#     try:
#         request = context['request']
#         print("Request", request)
#         print(request.META.get("HTTP_ACCEPT", ""))
#         print("final path:", os.path.join(settings.BASE_DIR, "static", img_url))
#
#         if "image/webp" in request.META.get("HTTP_ACCEPT", ""):
#             webp_static_path = settings.STATIC_URL + img_url.rsplit('.', 1)[0] + '.webp'
#             webp_file_path = os.path.join(settings.BASE_DIR, "static", img_url.rsplit('.', 1)[0] + '.webp')
#             print("static", webp_static_path)
#             print("file", webp_file_path)
#
#             if os.path.exists(webp_file_path):
#                 return webp_static_path
#             else:
#                 convert_to_webp(os.path.join(settings.BASE_DIR, "static", img_url))
#         return static_path
#     except KeyError:
#         return static_path
#
#
#
# import os.path
# from pickletools import optimize
#
# absolute_path = r"E:\BikeRental\bike-rental-django\WildWheel\core\static\images\background_img2.jpg"
#
# from PIL import Image
#
# def convert_to_webp(filename, path=absolute_path):
#     """
#     Converts an image to WebP format if it is not already in that format.
#     Returns the path to the converted image.
#     """
#     extension = filename.split('.')[-1].lower()
#     fname = filename.split('.')[0]
#
#     if not os.path.exists(path):
#         print(f"Eror: The file {path} does not exist.")
#         return None
#
#     img = Image.open(path)
#     print("Image opened:", img)
#     webp_path = os.path.splitext(path)[0] + '.webp'
#
#     if extension == "png" or extension == "jpg" or extension == "jpeg":
#         print("Webpath:", webp_path)
#         img.save(webp_path, "WEBP", quality=75, optimize=True)
#         return webp_path
#
#
# convert_to_webp("background_img2.jpg")