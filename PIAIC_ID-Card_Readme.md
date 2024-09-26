
# PIAIC Dynamic ID Card Creation Using Python

![Generated ID Card](PIAIC_ID_Card.png)


## Project Overview

This project demonstrates how to create a dynamic ID card using Python. The ID card includes user-specific details, a QR code, an uploaded image, and a watermark. The final card is saved in PNG format and can be displayed and downloaded directly from Google Colab.

### Technologies Used:
- Python
- Google Colab
- Libraries: `qrcode`, `PIL`, `matplotlib`, `google.colab`

## Steps to Create the ID Card

### 1. Import Necessary Libraries

We start by importing the required libraries:
```python
import qrcode 
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from google.colab import files
```

### 2. Define User Details

Define the user details like name, roll number, location, etc. These details will be used on the ID card.
```python
# User details
name = "Muhammad Danish"
roll_no = "PIAIC 345"
location = "Karachi"
distance_learning = "No"
day_time = "Sunday 09:00 to 01:00"
batch_no = "61 Morning"
signature_text = "Authorized Signature"
```

### 3. Create the ID Card Function

The function `create_id_card()` is defined to generate the ID card. It handles:
- Drawing a background with a sky blue header and footer.
- Adding text like the user's name, roll number, and location.
- Uploading and adding a user picture and a PIAIC watermark.
- Generating a QR code from the user’s details.
- Adding a signature field in the footer.

```python
def create_id_card(name, roll_no, location, distance_learning, day_time, batch_no, image_path, watermark_path):
    width, height = 600, 400
    id_card = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(id_card)

    # Rounded rectangle
    draw.rounded_rectangle([0, 0, width, height], radius=20, outline="black", width=5)

    # Header and footer colors
    header_color = (135, 206, 235)
    footer_color = (135, 206, 235)
    draw.rectangle([0, 0, width, 50], fill=header_color)
    draw.rectangle([0, height - 50, width, height], fill=footer_color)

    # Fonts
    try:
        font_large = ImageFont.truetype("Arial Rounded MT Bold.ttf", 36)
        font_medium = ImageFont.truetype("Arial Rounded MT Bold.ttf", 28)
    except OSError:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        print("Error loading specified font. Using default font.")
    
    # Add text
    draw.text((40, 10), "PIAIC ID Card", fill="white", font=font_large)
    draw.text((40, 70), f"Name: {name}", fill="black", font=font_medium)
    draw.text((40, 110), f"Roll No: {roll_no}", fill="black", font=font_medium)
    draw.text((40, 150), f"Location: {location}", fill="black", font=font_medium)
    draw.text((40, 190), f"Distance Learning: {distance_learning}", fill="black", font=font_medium)
    draw.text((40, 230), f"Day/Time: {day_time}", fill="black", font=font_medium)
    draw.text((40, 270), f"Batch No: {batch_no}", fill="black", font=font_medium)
    
    # Add watermark
    try:
        watermark = Image.open(watermark_path)
        watermark = watermark.resize((width, height), Image.LANCZOS)
        id_card = Image.blend(id_card.convert("RGBA"), watermark, alpha=0.1)
    except Exception as e:
        print(f"Error loading watermark: {e}")
        return None

    # Add user picture
    try:
        image = Image.open(image_path)
        image = image.resize((120, 120))
        id_card.paste(image, (400, 20))
    except Exception as e:
        print(f"Error loading user picture: {e}")
        return None
    
    # Generate QR code
    qr_data = f"{name}, {roll_no}, {location}, {distance_learning}, {day_time}, {batch_no}"
    qr = qrcode.make(qr_data)
    qr = qr.resize((120, 120))
    id_card.paste(qr, (400, 160))

    # Signature text in footer
    text_bbox = draw.textbbox((0, 0), signature_text, font=font_medium)
    text_width = text_bbox[2] - text_bbox[0]
    draw.text(((width - text_width) / 2, height - 45), signature_text, fill="black", font=font_medium)
    draw.line([(40, height - 30), (width - 40, height - 30)], fill="black", width=2)

    # Save the ID card
    id_card_path = "/content/PIAIC_ID_Card.png"
    id_card.save(id_card_path)

    return id_card_path
```

### 4. Upload User Picture and Watermark

To personalize the card, the user is prompted to upload their picture and the PIAIC watermark.

```python
print("Upload your picture:")
uploaded = files.upload()
image_path = list(uploaded.keys())[0]

print("Upload the PIAIC watermark image:")
watermark_uploaded = files.upload()
watermark_path = list(watermark_uploaded.keys())[0]
```

### 5. Generate and Display the ID Card

Finally, we create and display the ID card using `matplotlib`. If the card is generated successfully, it is also available for download.

```python
id_card_path = create_id_card(name, roll_no, location, distance_learning, day_time, batch_no, image_path, watermark_path)

if id_card_path:
    plt.imshow(Image.open(id_card_path))
    plt.axis('off')
    plt.show()

    files.download(id_card_path)
else:
    print("ID card creation failed.")
```

---

You can adjust the code or explanation as needed for your repository. Be sure to add the generated ID card image to the repository for it to display correctly at the top of the Markdown file.
