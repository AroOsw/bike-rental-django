from PIL import Image, ExifTags
import os

EXIF_ORIENTATION_TAG = 274

save_path = r"E:\BikeRental\bike-rental-django\core\static\converted"
dir_path = r"E:\BikeRental\bike-rental-django\core\static\to convert"
# photo_path = r"E:\BikeRental\bike-rental-django\core\static\images\gallery2.jpg"


def autocorrect_image_orientation(img):
    """
    Obraca obraz PIL, jeśli jest to wymagane na podstawie metadanych EXIF.

    Args:
        img (PIL.Image): Obiekt obrazu PIL.

    Returns:
        PIL.Image: Obrócony obraz lub oryginalny, jeśli obrót nie był potrzebny.
    """
    try:
        # 1. Pobierz metadane EXIF
        exif = img._getexif()

        # 2. Sprawdź, czy istnieją metadane i znacznik orientacji
        if exif is not None:
            # Mapowanie tagów EXIF na ich nazwy
            exif_data = {
                ExifTags.TAGS[k]: v
                for k, v in exif.items()
                if k in ExifTags.TAGS
            }
            orientation = exif_data.get('Orientation')

            # 3. Wykonaj obrót na podstawie wartości orientacji
            transpose_operations = {
                3: Image.ROTATE_180,  # Wartość 3: obrót o 180 stopni
                6: Image.ROTATE_270,  # Wartość 6: obrót o 270 stopni (czyli 90 w prawo)
                8: Image.ROTATE_90,  # Wartość 8: obrót o 90 stopni (czyli 90 w lewo)
            }

            if orientation in transpose_operations:
                img = img.transpose(transpose_operations[orientation])


    except (AttributeError, KeyError, IndexError):
        pass

    return img


def process_photos(directory_path, save_path):
    if os.path.exists(directory_path):
        photo_list = os.listdir(directory_path)
        for photo in photo_list:
            if not photo.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                continue  # Pomiń pliki, które nie są obrazami

            try:
                # Otwieranie obrazu
                # Użycie os.path.join jest bezpieczniejsze niż f"{...}\{...}"
                full_path = os.path.join(directory_path, photo)
                img = Image.open(full_path)

                # >>> WAŻNE: KOREKTA ORIENTACJI JAKO PIERWSZY KROK <<<
                img = autocorrect_image_orientation(img)

                # Tworzenie nazwy pliku i zapis
                name = photo.split(".")[0] + ".webp"
                save_full_path = os.path.join(save_path, name)

                # Zapis do WEBP
                img.save(save_full_path, "WEBP", quality=85, optimize=True)

                print(f"Obrócono: {photo} -> {name}")

            except Exception as e:
                print(f"Błąd przetwarzania pliku {photo}: {e}")

process_photos(dir_path, save_path)


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

# if os.path.exists(photo_path):
#     img = Image.open(photo_path)
#     file_name = os.path.basename(photo_path)
#     name = os.path.splitext(file_name)[0] + ".webp"
#     img.save(os.path.join(save_path, name), "WEBP", quality=75, optimize=True)
# else:
#     print(f"File not found: {photo_path}")

