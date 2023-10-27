import os
import shutil
from sklearn.model_selection import train_test_split
import numpy as np

# Define input folders and output base directory
image_folder = "./ColorImage_Pan"
mask_folder = "./Annotated_Pan"
output_base_dir = "TrainingDataset_Pan"

# Get the list of image and mask file names
image_files = os.listdir(image_folder)
mask_files = os.listdir(mask_folder)

# Ensure image and mask pairs are in the same order
image_files.sort()
mask_files.sort()
assert len(image_files) == len(mask_files), "Images and masks should have the same number of elements."

# Shuffle the pairs
combined_data = list(zip(image_files, mask_files))
np.random.shuffle(combined_data)

# Unzip the shuffled pairs
shuffled_images, shuffled_masks = zip(*combined_data)

# Calculate the number of samples for each set
total_samples = len(shuffled_images)
train_samples = int(0.8 * total_samples)
val_samples = int(0.1 * total_samples)
test_samples = total_samples - train_samples - val_samples

# Split the data into train, validation, and test sets
train_images, remaining_images, train_masks, remaining_masks = train_test_split(
    shuffled_images, shuffled_masks, train_size=train_samples, stratify=None, random_state=42)

val_images, test_images, val_masks, test_masks = train_test_split(
    remaining_images, remaining_masks, test_size=0.5, stratify=None, random_state=42)

# Function to create directories and copy files
def organize_data(images, masks, dest_base_dir, split):
    dest_image_dir = os.path.join(dest_base_dir, 'Images', split)
    dest_mask_dir = os.path.join(dest_base_dir, 'Masks', split)
    os.makedirs(dest_image_dir, exist_ok=True)
    os.makedirs(dest_mask_dir, exist_ok=True)

    for image_file, mask_file in zip(images, masks):
        shutil.copy(os.path.join(image_folder, image_file), os.path.join(dest_image_dir, image_file))
        shutil.copy(os.path.join(mask_folder, mask_file), os.path.join(dest_mask_dir, mask_file))

# Organize the data into train, validation, and test sets
organize_data(train_images, train_masks, output_base_dir, 'train')
organize_data(val_images, val_masks, output_base_dir, 'validation')
organize_data(test_images, test_masks, output_base_dir, 'test')

print("Data organized and copied to respective folders.")