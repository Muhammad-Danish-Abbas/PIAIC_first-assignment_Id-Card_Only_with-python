import qrcode
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from google.colab import files

# User details
name = "Muhammad Danish"
roll_no = "PIAIC 345"
location = "Karachi"
distance_learning = "No"
day_time = "Sunday 09:00 to 01:00"
batch_no = "61 Morning"
signature_text = "Authorized Signature"  # Updated text

# Function to create ID card with custom font and colors
def create_id_card(name, roll_no, location, distance_learning, day_time, batch_no, image_path, watermark_path):
    # Create an ID card background
    width, height = 600, 400  # Adjusted height
    id_card = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(id_card)

    # Add rounded rectangle background
    draw.rounded_rectangle([0, 0, width, height], radius=20, outline="black", width=5)

    # Change header and footer color to sky blue
    header_color = (135, 206, 235)  # Sky Blue
    footer_color = (135, 206, 235)
    draw.rectangle([0, 0, width, 50], fill=header_color)
    draw.rectangle([0, height - 50, width, height], fill=footer_color)

    # Load custom font
    try:
        font_large = ImageFont.truetype("Arial Rounded MT Bold.ttf", 36)
        font_medium = ImageFont.truetype("Arial Rounded MT Bold.ttf", 28)
    except OSError:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        print("Error loading specified font. Using default font.")

    # Add text to ID card
    draw.text((40, 10), "PIAIC ID Card", fill="white", font=font_large)
    draw.text((40, 70), f"Name: {name}", fill="black", font=font_medium)
    draw.text((40, 110), f"Roll No: {roll_no}", fill="black", font=font_medium)
    draw.text((40, 150), f"Location: {location}", fill="black", font=font_medium)
    draw.text((40, 190), f"Distance Learning: {distance_learning}", fill="black", font=font_medium)
    draw.text((40, 230), f"Day/Time: {day_time}", fill="black", font=font_medium)
    draw.text((40, 270), f"Batch No: {batch_no}", fill="black", font=font_medium)

    # Add watermark
    if watermark_path:
        try:
            watermark = Image.open(watermark_path)
            watermark = watermark.resize((width, height), Image.LANCZOS)
            if watermark.mode != 'RGBA':
                watermark = watermark.convert("RGBA")
            id_card = Image.blend(id_card.convert("RGBA"), watermark, alpha=0.1)
        except Exception as e:
            print(f"Error loading watermark: {e}")
            return None

    # Add user picture to ID card
    if image_path:
        try:
            image = Image.open(image_path)
            image = image.resize((120, 120))  # Increased image size for better visibility
            id_card.paste(image, (400, 20))
        except Exception as e:
            print(f"Error loading user picture: {e}")
            return None

    # Generate QR code
    qr_data = f"{name}, {roll_no}, {location}, {distance_learning}, {day_time}, {batch_no}"
    qr = qrcode.make(qr_data)
    qr = qr.resize((120, 120))
    id_card.paste(qr, (400, 160))

# Add signature text in the footer
    #text_width, text_height = draw.textsize(signature_text, font=font_medium)  # Get width and height - this method is deprecated
    text_bbox = draw.textbbox((0, 0), signature_text, font=font_medium) # Calculate the bounding box of the text
    text_width = text_bbox[2] - text_bbox[0] # Calculate width of text based on bounding box
    text_height = text_bbox[3] - text_bbox[1] # Calculate height of text based on bounding box
    draw.text(((width - text_width) / 2, height - 45), signature_text, fill="black", font=font_medium)  # Centered in footer
    draw.line([(40, height - 30), (width - 40, height - 30)], fill="black", width=2)  # Signature line in footer

    # Save ID card
    id_card_path = "/content/PIAIC_ID_Card.png" #removed indentation
    id_card.save(id_card_path)

    return id_card_path # Added indentation so that these lines are part of the create_id_card function

# Upload your picture and watermark image
print("Upload your picture:")
uploaded = files.upload()
image_path = list(uploaded.keys())[0]

print("Upload the PIAIC watermark image:")
watermark_uploaded = files.upload()
watermark_path = list(watermark_uploaded.keys())[0]

# Create the ID card
id_card_path = create_id_card(name, roll_no, location, distance_learning, day_time, batch_no, image_path, watermark_path)

# Check if the ID card was created successfully
if id_card_path:
    # Display the ID card
    plt.imshow(Image.open(id_card_path))
    plt.axis('off')
    plt.show()

    # Download the ID card
    files.download(id_card_path)
else:
    print("ID card creation failed.")