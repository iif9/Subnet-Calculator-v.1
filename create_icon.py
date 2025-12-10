from PIL import Image, ImageDraw, ImageFont
import os

# إنشاء أيقونة بحجم 256x256
size = 256
image = Image.new('RGB', (size, size), color=(0x08, 0x29, 0x46))  # Dark blue background

draw = ImageDraw.Draw(image)

# رسم دائرة زرقاء فاتحة
circle_color = (0x26, 0x4C, 0x8C)  # Light blue
draw.ellipse([20, 20, size-20, size-20], fill=circle_color, outline=(0x4C, 0x7A, 0xC8), width=3)

# محاولة استخدام خط (سيتم استخدام الخط الافتراضي إذا لم يتوفر)
try:
    font = ImageFont.truetype("arial.ttf", 80)
except:
    font = ImageFont.load_default()

# رسم الحرف "S" للـ Subnet
text = "S"
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x = (size - text_width) // 2
y = (size - text_height) // 2 - 10

draw.text((x, y), text, fill=(255, 255, 255), font=font)

# حفظ الأيقونة
icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')
image.save(icon_path, 'PNG')

print(f"Icon created successfully at: {icon_path}")
