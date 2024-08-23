from src.app_tools.yaml_loader import load_yaml_file

from PIL import Image, ImageDraw, ImageOps


def convert_to_png(image_path, output_path):
    # Open an image file
    with Image.open(image_path) as img:
        # Convert image to PNG
        img = img.convert("RGBA")
        # Save it as PNG
        img.save(output_path, "PNG")


def resize_image(image_path, output_path, size):
    # Open an image file
    with Image.open(image_path) as img:
        # Resize the image using LANCZOS resampling
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        # Save the resized image
        img.save(output_path)


def round_corners(image_path, output_path, radius):
    # Open an image file
    with Image.open(image_path) as img:
        # Create a mask to round the corners
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0) + img.size, radius, fill=255)

        # Apply the rounded mask to the image
        img_rounded = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        img_rounded.putalpha(mask)

        # Save the image with rounded corners
        img_rounded.save(output_path, format="PNG")


def format_images():
    # Get medal details
    yaml_file_path = "conf/medal_details/medal_details_numeric.yaml"
    medal_details_numeric = load_yaml_file(yaml_file_path)

    yaml_file_path = "conf/medal_details/medal_details_categorical.yaml"
    medal_details_categorical = load_yaml_file(yaml_file_path)

    yaml_file_path = "conf/medal_details/medal_details_binary.yaml"
    medal_details_binary = load_yaml_file(yaml_file_path)

    yaml_file_path = "conf/medal_details/medal_details_special.yaml"
    medal_details_special = load_yaml_file(yaml_file_path)

    # Combine medals
    medals_dict = {
        **medal_details_numeric,
        **medal_details_categorical,
        **medal_details_binary,
        **medal_details_special,
    }

    for medal_name in list(medals_dict.keys()):
        url_jpg = medals_dict[medal_name]["image_path"]
        url_png = url_jpg.replace("jpeg", "png").replace("jpg", "png")
        size = 500  # New size in pixels
        radius = 30  # Radius for rounded corners

        input_image_path = url_jpg
        output_image_path = url_png

        # Convert to PNG
        convert_to_png(input_image_path, "temp.png")

        # Resize Image
        resize_image("temp.png", "resized.png", size)

        # Round Corners
        round_corners("resized.png", output_image_path, radius)
    return
