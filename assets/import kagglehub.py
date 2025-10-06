import kagglehub

# Download latest version
path = kagglehub.dataset_download("sumairaziz/vibration-faults-dataset-for-rotating-machines")

print("Path to dataset files:", path)
