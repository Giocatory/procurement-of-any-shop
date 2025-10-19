from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image():
    # Создаем изображение 300x200
    img = Image.new('RGB', (300, 200), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    
    # Добавляем текст
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    text = "No Image"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (300 - text_width) / 2
    y = (200 - text_height) / 2
    
    draw.text((x, y), text, fill=(180, 180, 180), font=font)
    
    # Сохраняем
    os.makedirs("static/images", exist_ok=True)
    img.save("static/images/placeholder.jpg")
    print("Placeholder image created!")

if __name__ == "__main__":
    create_placeholder_image()