from PIL import Image
import os


save_path = r"E:\BikeRental\bike-rental-django\core\static\webp_images"
# directory_path = r"E:\BikeRental\bike-rental-django\core\static\images"
photo_path = r"E:\BikeRental\bike-rental-django\core\static\images\20250913_095908.jpg"
#
#
# if os.path.exists(directory_path):
#     photo_list = os.listdir(directory_path)
#     for photo in photo_list:
#         if photo == "background_img2.jpg":
#             img = Image.open(rf"{directory_path}\{photo}")
#             img = img.resize((1920,1080))
#             name = photo.split(".")[0] + ".webp"
#             img.save(rf"{save_path}\{name}", "WEBP", quality=80, optimize=True)
#         else:
#             img = Image.open(rf"{directory_path}\{photo}")
#             img = img.resize((400, 400))
#             name = photo.split(".")[0] + ".webp"
#             img.save(rf"{save_path}\{name}", "WEBP", quality=85, optimize=True)

if os.path.exists(photo_path):
    img = Image.open(photo_path)
    file_name = os.path.basename(photo_path)
    name = os.path.splitext(file_name)[0] + ".webp"
    img.save(os.path.join(save_path, name), "WEBP", quality=75, optimize=True)
else:
    print(f"File not found: {photo_path}")




