from openni import openni2
# OpenNI'yı başlat
openni2.initialize()

# Cihazı aç
device = openni2.Device.open_any()

# Derinlik stream'ini aç
depth_stream = device.create_depth_stream()
depth_stream.start()

# Derinlik verisini al
frame = depth_stream.read_frame()

# Derinlik verisini işle (örneğin, veriyi görselleştir)
depth_array = frame.get_buffer_as_uint16()
# Burada derinlik verisini kullanabilirsiniz, örneğin, OpenCV ile görselleştirebilirsiniz

# Stream'leri kapat ve OpenNI'yı kapat
depth_stream.stop()
depth_stream.destroy()
device.close()
openni2.unload()