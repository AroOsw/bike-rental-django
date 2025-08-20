from PIL import Image
import os

directory_path = r"E:\BikeRental\bike-rental-django\WildWheel\core\static\images"
save_path = r"E:\BikeRental\bike-rental-django\WildWheel\core\static\webp_images"

if os.path.exists(directory_path):
    photo_list = os.listdir(directory_path)
    for photo in photo_list:
        if photo == "background_img2.jpg":
            img = Image.open(rf"{directory_path}\{photo}")
            img = img.resize((1920,1080))
            name = photo.split(".")[0] + ".webp"
            img.save(rf"{save_path}\{name}", "WEBP", quality=80, optimize=True)
        else:
            img = Image.open(rf"{directory_path}\{photo}")
            img = img.resize((400, 400))
            name = photo.split(".")[0] + ".webp"
            img.save(rf"{save_path}\{name}", "WEBP", quality=70, optimize=True)





