
import itertools

# Imports
import pandas as pd
import numpy as np
import os
import random
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import itertools 

def apply_sepia_filter(image):
    width, height = image.size
    pixels = image.load()  # Create the pixel map
    for py in range(height):
        for px in range(width):
            r, g, b = image.getpixel((px, py))
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            tr = min(255, tr)
            tg = min(255, tg)
            tb = min(255, tb)
            pixels[px, py] = (tr, tg, tb)
    return image


def generate_images(image_dir, image_base):
    images = os.listdir(image_dir)
    random.shuffle(images)  # Shuffle to randomize which images get the filter
    sepia_indices = np.random.choice(len(images), len(images) // 2, replace=False)
    data_for_csv = []
    for index, filename in enumerate(images):
        file_path = image_dir + '/' + filename
        try:
            image = Image.open(file_path)  # Attempt to open the image
        except IOError:
            continue  # Skip files that are not images

        is_sepia = 0
        if index in sepia_indices:
            image = apply_sepia_filter(image)
            sepia_file_path = image_base + '/' + f"sepia_{filename}"
            print(sepia_file_path)
            image.save(sepia_file_path)
            file_path = sepia_file_path
            print('!')
            is_sepia = 1
        else:
            non_sepia_file_path = f"{image_base}/not_sepia_{filename}"
            print(non_sepia_file_path)
            image.save(non_sepia_file_path)
            file_path = non_sepia_file_path
            print('!!')

        data_for_csv.append([file_path, is_sepia])

    # Save to CSV
    df = pd.DataFrame(data_for_csv, columns=['file_path', 'is_sepia'])
    csv_path = 'image_labels.csv'
    df.to_csv(csv_path, index=False)
    print(f"Data saved to {csv_path}")
    print(df.values)


def delete_all_images(image_base):
    for filename in os.listdir(image_base):
        if filename.startswith('sepia_') or filename.startswith('not_sepia_'):
            os.remove(f"{image_base}/{filename}")


delete_all_images(image_base='images')


generate_images('images/trainingBaseData', 'images')

def print_images_in_grid(image_type, image_dir, grid_width=5):
    if image_type == 'sepia':
        images = [f for f in os.listdir(image_dir) if f.startswith('sepia_')]
    else:
        images = [f for f in os.listdir(image_dir) if f.startswith('not_sepia_')]

    random.shuffle(images)  # Shuffle the list to display random images

    # Calculate grid size
    if len(images) < grid_width:
        grid_width = len(images)
    grid_height = int(len(images) / grid_width) + (len(images) % grid_width > 0)

    # Create figure with sub-plots
    fig, axes = plt.subplots(grid_height, grid_width, figsize=(grid_width * 3, grid_height * 3))

    # Add each image to the sub-plot
    for i, ax in enumerate(axes.flat):
        if i < len(images):
            img_path = os.path.join(image_dir, images[i])
            img = Image.open(img_path)
            ax.imshow(img)
            ax.set_title(images[i])
            ax.axis('off')  # Hide the axes ticks
        else:
            ax.axis('off')  # Hide the axes ticks if no more images

    plt.show()  # Display the figure with images

