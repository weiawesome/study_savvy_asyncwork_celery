def rotate_image_based_on_exif(image):
    try:
        exif_data = image._getexif()
        if exif_data:
            orientation_tag = 0x0112
            if orientation_tag in exif_data:
                orientation = exif_data[orientation_tag]
                if orientation == 3:
                    image = image.rotate(180,expand=True)
                elif orientation == 6:
                    image = image.rotate(-90,expand=True)
                elif orientation == 8:
                    image = image.rotate(90,expand=True)
    except AttributeError:
        print(AttributeError.name)

    return image