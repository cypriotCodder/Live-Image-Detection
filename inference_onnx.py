from ultralytics import YOLO

# Load the ONNX model
# The YOLO class can automatically detect and load ONNX models
model = YOLO("best.onnx")

# Run inference on the image
# task='detect' is often inferred, but good to be explicit if needed. 
# For ONNX, the arguments are similar to the PyTorch model.
results = model.predict("test.png", save=True)

# Show the results (if running in a GUI environment)
results[0].show()

print("Inference completed. Results saved.")
print(results)
