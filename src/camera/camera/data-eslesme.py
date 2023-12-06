import os
import cv2  # Görüntü işleme kütüphanesi

# Renkli ve siyah beyaz maskelenmiş görüntüleri içeren klasörleri tanımlayın
renkli_klasor = "/home/gizemgunes/Desktop/dataset/train"
siyah_beyaz_klasor = "/home/gizemgunes/Desktop/dataset/test"

renkli_goruntuler = os.listdir(renkli_klasor)
siyah_beyaz_maskeler = os.listdir(siyah_beyaz_klasor)

veri_seti = []

# Görüntüleri eşleştirme ve veri setine ekleme
for renkli, siyah_beyaz in zip(renkli_goruntuler, siyah_beyaz_maskeler):
    renkli_resim = cv2.imread(os.path.join(renkli_klasor, renkli))
    siyah_beyaz_resim = cv2.imread(os.path.join(siyah_beyaz_klasor, siyah_beyaz), cv2.IMREAD_GRAYSCALE)

    # Gerekli işlemler yapılabilir, örneğin boyutları ayarlama veya normalizasyon

    veri_seti.append((renkli_resim, siyah_beyaz_resim))

# Veri setini karıştırma
import random

random.shuffle(veri_seti)

# Eğitim, doğrulama ve test setlerine ayırma
egitim_seti = veri_seti[:int(0.7 * len(veri_seti))]
dogrulama_seti = veri_seti[int(0.7 * len(veri_seti)):int(0.85 * len(veri_seti))]
test_seti = veri_seti[int(0.85 * len(veri_seti)):]

# Modelinize giriş ve çıkışları vermek için veri setini hazır hale getirin
# Bu adımlar, model eğitimi öncesinde verileri uygun formata dönüştürmeyi içerebilir.
# (Örneğin, verileri normalleştirme, boyutlandırma veya tensorlara dönüştürme)

# Model eğitimi için hazır veri seti kullanılabilir.
