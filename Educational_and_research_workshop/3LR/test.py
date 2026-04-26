import os
import time
from PIL import Image
import io

def compress_png(image_path):
    """Сжатие изображения в формат PNG"""
    img = Image.open(image_path)
    buffer = io.BytesIO()
    start = time.perf_counter()
    img.save(buffer, format='PNG', optimize=True)
    elapsed = time.perf_counter() - start
    size = len(buffer.getvalue())
    return size, elapsed

def compress_webp_lossless(image_path):
    """Сжатие изображения в формат WebP (lossless)"""
    img = Image.open(image_path)
    buffer = io.BytesIO()
    start = time.perf_counter()
    img.save(buffer, format='WEBP', lossless=True, quality=100)
    elapsed = time.perf_counter() - start
    size = len(buffer.getvalue())
    return size, elapsed

def get_file_size(file_path):
    return os.path.getsize(file_path)

# Список тестовых изображений
test_images = ['image_photo.jpg', 'image_screenshot.png', 'image_icons.png']

# Создаём тестовые изображения если нет
for name in test_images:
    if not os.path.exists(name):
        img = Image.new('RGB', (1920, 1080), color='white')
        img.save(name)

print("=" * 70)
print("ЭКСПЕРИМЕНТ: СРАВНЕНИЕ СЖАТИЯ ИЗОБРАЖЕНИЙ (PNG vs WebP Lossless)")
print("=" * 70)

results = []

for img_path in test_images:
    original_size = get_file_size(img_path)
    
    # Сжатие в PNG
    png_size, png_time = compress_png(img_path)
    png_ratio = original_size / png_size
    
    # Сжатие в WebP
    webp_size, webp_time = compress_webp_lossless(img_path)
    webp_ratio = original_size / webp_size
    
    results.append({
        'name': img_path,
        'original': original_size,
        'png_size': png_size,
        'png_ratio': png_ratio,
        'png_time': png_time,
        'webp_size': webp_size,
        'webp_ratio': webp_ratio,
        'webp_time': webp_time
    })
    
    print(f"\nФайл: {img_path}")
    print(f"   Исходный размер: {original_size:,} байт ({original_size/1024:.1f} KB)")
    print(f"\n   PNG: размер={png_size:,} байт, коэф={png_ratio:.1f}x, время={png_time:.4f}с")
    print(f"   WebP: размер={webp_size:,} байт, коэф={webp_ratio:.1f}x, время={webp_time:.4f}с")

# Итоговая таблица
print("\n" + "=" * 70)
print("СВОДНАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ")
print("=" * 70)
print(f"{'Изображение':<20} {'Исходный':<12} {'PNG':<25} {'WebP':<25}")
print(f"{'':20} {'(KB)':<12} {'размер/коэф/время':<25} {'размер/коэф/время':<25}")
print("-" * 82)

for r in results:
    name = r['name'][:18]
    original_kb = r['original'] / 1024
    png_kb = r['png_size'] / 1024
    webp_kb = r['webp_size'] / 1024
    print(f"{name:<20} {original_kb:<12.1f} {png_kb:.1f}/ {r['png_ratio']:.1f}x/ {r['png_time']:.3f}s   {webp_kb:.1f}/ {r['webp_ratio']:.1f}x/ {r['webp_time']:.3f}s")