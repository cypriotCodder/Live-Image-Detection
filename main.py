from ultralytics import YOLO
import torch

# Check for CUDA device and set it
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using device: {device}')

if device == 'cpu':
    print("CUDA is not available. Training will run on CPU, which might be slow.")

model = YOLO("yolov8n.pt")

#train the model
model.train(data="coco128.yaml", epochs=100, imgsz=640, device=device)

#evaluate the model
model.val(data="coco128.yaml", imgsz=640)

results = model.predict("test.png", save=True)
results[0].show()

print(results)

model.save("yolov8n.pt")