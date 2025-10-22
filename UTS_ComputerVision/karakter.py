import cv2
import numpy as np
import os

# Pastikan folder output ada
os.makedirs("output", exist_ok=True)

# 1. Membuat kanvas kosong hitam (300x300 pixel)
canvas = np.zeros((300, 300, 3), dtype=np.uint8)

# === Membuat karakter: KUCING ===
# Kepala (lingkaran)
cv2.circle(canvas, (150, 150), 70, (128, 128, 128), -1)  # kepala abu-abu

# Telinga kiri & kanan (segitiga)
telinga_kiri = np.array([[90, 100], [120, 50], [130, 110]], np.int32)
telinga_kanan = np.array([[170, 110], [180, 50], [210, 100]], np.int32)
cv2.fillPoly(canvas, [telinga_kiri], (100, 100, 100))
cv2.fillPoly(canvas, [telinga_kanan], (100, 100, 100))

# Mata kiri dan kanan
cv2.circle(canvas, (125, 145), 10, (255, 255, 255), -1)  # putih mata
cv2.circle(canvas, (175, 145), 10, (255, 255, 255), -1)
cv2.circle(canvas, (125, 145), 4, (0, 0, 0), -1)         # pupil
cv2.circle(canvas, (175, 145), 4, (0, 0, 0), -1)

# Hidung segitiga kecil
hidung = np.array([[145, 165], [155, 165], [150, 170]], np.int32)
cv2.fillPoly(canvas, [hidung], (0, 128, 255))

# Mulut (garis)
cv2.line(canvas, (150, 170), (150, 185), (0, 0, 0), 2)
cv2.line(canvas, (150, 185), (140, 195), (0, 0, 0), 2)
cv2.line(canvas, (150, 185), (160, 195), (0, 0, 0), 2)

# Kumis kiri dan kanan
for i in range(3):
    cv2.line(canvas, (140, 165 + i * 5), (100, 160 + i * 5), (255, 255, 255), 1)
    cv2.line(canvas, (160, 165 + i * 5), (200, 160 + i * 5), (255, 255, 255), 1)

# Simpan karakter asli
cv2.imwrite("output/karakter.png", canvas)

# === 2. Transformasi ===

# Translasi (geser karakter)
M_translate = np.float32([[1, 0, 50], [0, 1, 30]])
translated = cv2.warpAffine(canvas, M_translate, (300, 300))
cv2.imwrite("output/translate.png", translated)

# Rotasi
M_rotate = cv2.getRotationMatrix2D((150, 150), 30, 1)
rotated = cv2.warpAffine(canvas, M_rotate, (300, 300))
cv2.imwrite("output/rotate.png", rotated)

# Resize (ubah ukuran jadi 150x150)
resized = cv2.resize(canvas, (150, 150))
cv2.imwrite("output/resize.png", resized)

# Crop (potong bagian tengah)
crop = canvas[70:230, 90:210]
cv2.imwrite("output/crop.png", crop)

# === 3. Operasi bitwise ===
#Background default apabila tidak ada img/background.jpg
bg = np.full((300, 300, 3), (80, 80, 80), dtype=np.uint8)

#Jika ada img/background.jpg 
bg_path = "img/background.jpg"
if os.path.exists(bg_path):
    bg = cv2.imread(bg_path)
    bg = cv2.resize(bg, (300, 300))
    print("✅ Background ditemukan dan digunakan.")
else:
    print("⚠ Background tidak ditemukan, pakai default.")

# bitwise_and antara karakter dan background
bitwise = cv2.bitwise_and(canvas, bg)
cv2.imwrite("output/bitwise.png", bitwise)

# bitwise_or untuk efek gabungan akhir
final = cv2.bitwise_or(rotated, bg)
cv2.imwrite("output/final.png", final)

# === Tampilkan hasil di jendela ===
cv2.imshow("Karakter Kucing", canvas)
cv2.imshow("Rotate", rotated)
cv2.imshow("Crop", crop)
cv2.imshow("Bitwise", bitwise)
cv2.imshow("Final", final)

cv2.waitKey(0)
cv2.destroyAllWindows()
