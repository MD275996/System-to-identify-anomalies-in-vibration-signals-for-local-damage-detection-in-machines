import os
import pandas as pd
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "app/uploads"
PLOT_FOLDER = "app/static/tmp"

def save_file(file):
    # Ensure upload directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    return filename

def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return files

# def delete_file(filename):
#     file_path = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
#     if os.path.exists(file_path):
#         os.remove(file_path)
#         return True
#     return False

def delete_file(filename):
    filename = secure_filename(filename)
    plotname = filename.replace(".csv",".png")
    plot_path = os.path.join(PLOT_FOLDER, plotname)
    file_path = os.path.join(UPLOAD_FOLDER, filename)


    # 1. Plik musi istnieć
    if not os.path.exists(file_path):
        return False
    if os.path.exists(plot_path):
        os.remove(plot_path)
        
    # 2. Plik nie może być katalogiem
    if os.path.isdir(file_path):
        print("WARNING: Attempt to delete a directory, not a file!", file_path)
        return False

    # 3. Można dodać check rozszerzenia
    if not filename.lower().endswith(".csv"):
        print("WARNING: Attempt to delete non-CSV file!", filename)
        return False

    os.remove(file_path)
    return True

def generate_plot(filename):
    filename = secure_filename(filename)
    file_path = os.path.join(UPLOAD_FOLDER,filename)
    if not os.path.exists(file_path):
        return None
    df = pd.read_csv(file_path, header = None)
    column = df[0].to_numpy()
    plt.figure(figsize=(8,4))
    plt.plot(column, color='blue', linewidth=1)
    plt.title("Sygnał z impulsami i szumem")
    plt.xlabel("Próbka")
    plt.ylabel("Amplituda")
    plt.grid(True)
    plt.tight_layout()
    
    #zapisz w static/tmp
    output_name = filename.replace(".csv",".png")
    output_path = os.path.join(PLOT_FOLDER, output_name)
    plt.savefig(output_path)
    plt.close()

    return f"static/tmp/{output_name}"