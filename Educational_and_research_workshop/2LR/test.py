import gzip
import bz2
import time

def parse_size(size_str):
    """Переводит '100KB' в число байт"""
    if 'KB' in size_str:
        return int(size_str.replace('KB', '')) * 1024
    elif 'MB' in size_str:
        return int(size_str.replace('MB', '')) * 1024 * 1024
    return int(size_str)

def test_compression(data, method='gzip'):
    """Сжимает данные и замеряет время"""
    data_bytes = data.encode('utf-8')
    
    if method == 'gzip':
        start = time.time()
        compressed = gzip.compress(data_bytes)
        elapsed = time.time() - start
        return compressed, elapsed
    else:  # bz2
        start = time.time()
        compressed = bz2.compress(data_bytes)
        elapsed = time.time() - start
        return compressed, elapsed

# Список размеров для теста
sizes = ['100KB', '500KB', '1MB', '10MB', '50MB']

print("Сравнение сжатия Gzip и BZ2")
print("=" * 50)

for size in sizes:
    bytes_count = parse_size(size)
    # Создаём текст нужного размера
    text = "Lorem ipsum " * (bytes_count // 12 + 1)
    text = text[:bytes_count]
    
    # Тестируем Gzip
    comp_gzip, time_gzip = test_compression(text, 'gzip')
    ratio_gzip = len(text) / len(comp_gzip)
    
    # Тестируем BZ2
    comp_bz2, time_bz2 = test_compression(text, 'bz2')
    ratio_bz2 = len(text) / len(comp_bz2)
    
    print(f"\n{size}:")
    print(f"  Gzip: {time_gzip:.3f} сек, сжатие в {ratio_gzip:.1f} раз")
    print(f"  BZ2:  {time_bz2:.3f} сек, сжатие в {ratio_bz2:.1f} раз")
    print(f"  BZ2 медленнее в {time_bz2/time_gzip:.1f} раз, но сжимает лучше в {ratio_bz2/ratio_gzip:.1f} раз")