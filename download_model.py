import urllib.request

model1_url = "https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8n.pt"
model2_url = "https://huggingface.co/camenduru/shape_predictor_68_face_landmarks/resolve/main/shape_predictor_68_face_landmarks.dat"

model1_path = "yolov8n-face.pt"
model2_path = "shape_predictor_68_face_landmarks.dat"

print("Downloading YOLOv8 Face model...")
urllib.request.urlretrieve(model1_url, model2_path)
print("Downloading Dlib Face Landmarks model...")
urllib.request.urlretrieve(model2_url, model2_path)
print("Download complete!")
