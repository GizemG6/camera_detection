from sklearn.model_selection import train_test_split
import os

# Fotoğraf dizini
dataset_path = '/home/gizemgunes/Desktop/dataset'

# Tüm dosya yollarını al
file_paths = []
for root, dirs, files in os.walk(dataset_path):
    for file in files:
        file_paths.append(os.path.join(root, file))

# Etiketleri oluştur
labels = [1 if "siyah_beyaz" in path else 0 for path in file_paths]

# Veri setini eğitim ve test olarak bölelim (örneğin, %80 eğitim, %20 test)
train_files, test_files, train_labels, test_labels = train_test_split(file_paths, labels, test_size=0.2, random_state=42)

# Eğitim ve test setlerini işleyebilirsiniz
# Örneğin, TensorFlow'da bu fotoğrafları yükleyip modelinize besleyebilirsiniz
