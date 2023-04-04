import rosbag2_py
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message
import imageio
import numpy as np
import cv2
from time import perf_counter
from pathlib import Path, PurePath
import argparse
import random
import sys
import os
import shutil

"""
Création de gifs.

video = liste d'images

"""


def get_rosbag_options(path:str, serialization_format:str="cdr"):
    storage_options = rosbag2_py.StorageOptions(uri=path, storage_id="sqlite3")
    converter_options = rosbag2_py.ConverterOptions(
    input_serialization_format=serialization_format,output_serialization_format=serialization_format)
    return storage_options, converter_options

def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', action='store', type=str, dest='output',
                        default = "images_readme/gifs", help = 'Output folder name')
    parser.add_argument('-i','--input', action='store', type=str, dest='input',
                            help = 'Input file name (bag) or folder name',
                            default="database_presentation/location1")
    
    args = parser.parse_args()
    return args.input, args.output

def bag_to_video(source_bag)->list:
    # Ouverture des bags
    storage_options_in, converter_options_in = get_rosbag_options(str(source_bag))
    reader = rosbag2_py.SequentialReader()

    #Read
    reader.open(storage_options_in, converter_options_in)
    topic_types = reader.get_all_topics_and_types()
    type_map = {topic_types[i].name: topic_types[i].type for i in range(len(topic_types))}

    frames = []
    while reader.has_next():
        topic, data, t = reader.read_next()
        msg_type = get_message(type_map[topic])
        msg = deserialize_message(data, msg_type)
        
    # Enregistrement des images
        if topic == "/image_raw/compressed":
            # Décompression de l'image compressée
            np_arr = np.frombuffer(msg.data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if img is not None:    
                frames.append(img)
            else:
                print("BUG:image non décompressée")
    
    return frames

def video_to_gif(frames:list, output_file:Path, duration:int = 10, image_reduction:int = 1):
    """
    On sait le bag enregistré à 10 FPS
    standard duraction = 10s
    """
    start = perf_counter() #DEBUG
    fps = len(frames)/(duration*image_reduction)
    imageio.mimsave(output_file, frames[::image_reduction], fps = fps, loop = 0)

    print(f"Done saving file. It took: {perf_counter() - start} s") #DEBUG


def bag_to_gif(source_bag:Path, output_file:Path, duration:int = 10, image_reduction:int = 1):
    """
    On sait le bag enregistré à 10 FPS
    standard duraction = 10s
    n images = init_images / image_reuction
    """
    frames = bag_to_video(source_bag)
    print("Done reading bag. Saving file ...")
    video_to_gif(frames, output_file, duration, image_reduction)


def get_multiple_bags(source_folder:Path, amount_to_open: int, get_random:bool = False)->list:
    """
    Récupère les noms des n premiers bags d'un dossier.
    """
    if not isinstance(source_folder, PurePath): source_folder = Path(source_folder)
    bags = list(source_folder.glob("*.bag"))
    if len(bags) < amount_to_open:
        print(f"Not enough bags in folder (asked for {amount_to_open} but only {len(bags)}), returning all")
        return bags
    if get_random:
        return random.sample(bags, amount_to_open)
    bags.sort()
    return bags[:amount_to_open]

def concatene_images(images:list)->np.ndarray:
    """
    Concatène les images en une seule image.

    S'il en manque pour faire un carré, ajoute des 0
    """
    n_images = len(images)
    original_size = images[0].shape
    if n_images == 1:
        return images[0]
    elif n_images == 2:
        return cv2.hconcat(images)
    elif n_images <= 4:
        if n_images == 3: images.append(np.zeros_like(images[0]))
        concat_image = cv2.vconcat([cv2.hconcat(images[:2]), cv2.hconcat(images[2:])])
    elif n_images <= 9:
        for _ in range(9-n_images): images.append(np.zeros_like(images[0]))
        concat_image = cv2.vconcat([cv2.hconcat(images[:3]), cv2.hconcat(images[3:6]), cv2.hconcat(images[6:])])
    elif n_images <= 16:
        for _ in range(16-n_images): images.append(np.zeros_like(images[0]))
        concat_image = cv2.vconcat([cv2.hconcat(images[:4]), cv2.hconcat(images[4:8]), cv2.hconcat(images[8:12]), cv2.hconcat(images[12:])])
    elif n_images <= 25:
        for _ in range(25-n_images): images.append(np.zeros_like(images[0]))
        concat_image = cv2.vconcat([cv2.hconcat(images[:5]), cv2.hconcat(images[5:10]), cv2.hconcat(images[10:15]), cv2.hconcat(images[15:20]), cv2.hconcat(images[20:])])
    else:
        print("Too many images to concatenate. Return only with 25 images")
        return concatene_images(images[:25])
    concat_image = cv2.resize(concat_image, original_size[:2][::-1]) #Get shape and reverse it bcz cv2.resize wants the inverse of shape
    return concat_image


def extract_images_from_bag(source_bag:Path, destination_folder:Path, image_reduction:int = 1):
    frames = bag_to_video(source_bag)
    if not os.path.exists(destination_folder): os.makedirs(destination_folder)
    for i, frame in enumerate(frames[::image_reduction]):
        cv2.imwrite(destination_folder.joinpath(f"{i}.jpg").as_posix(), frame)

def extract_images_from_bags(source_folder:Path, destination_folder:Path, amount_to_open:int, image_reduction:int = 1,get_random:bool = False)->list:
    """
    Extrait les images de tous les bags et les enregistre dans des folders
    """
    bags_name = get_multiple_bags(source_folder, amount_to_open, get_random)
    for bag_name in bags_name:
        extract_images_from_bag(bag_name, destination_folder.joinpath(bag_name.stem), image_reduction)

def create_concatenate(source_folder:Path, destination_folder:Path):
    """
    Source folder contient tous les dossiers, chaque dossier contient les images d'un bag.
    JE DOIS AVOIR FILTRER AVANT POUR QU'IL Y AIT LE MEME NOMBRE D'IMAGES DANS CHAQUE DOSSIER
    """
    images_folders = [folder for folder in source_folder.iterdir()]
    n_images = len(list(images_folders[0].iterdir()))
    if not os.path.exists(destination_folder): os.makedirs(destination_folder)
    for i in range(n_images):
        images = [cv2.imread(str(folder.joinpath(f"{i}.jpg"))) for folder in images_folders]
        concat_image = concatene_images(images)
        cv2.imwrite(destination_folder.joinpath(f"{i}.jpg").as_posix(), concat_image)

def load_images_from_folder(temp_folder_for_concatene:Path):
    image_files = sorted(temp_folder_for_concatene.glob('*.jpg'), key=lambda x: int(x.stem))
    images = []
    for filename in image_files:
        img = cv2.imread(filename.as_posix())
        if img is not None:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            images.append(img_rgb)
    return images

def complete_process_to_be_renamed(source_folder, destination_path, amount_to_open, image_reduction:int = 1, get_random:bool = False):
    temp_folder_for_bags = Path("Temp")
    temp_folder_for_concatene = Path("Temp_concatene")
    extract_images_from_bags(source_folder, temp_folder_for_bags, amount_to_open, image_reduction, get_random) #Reduction d'images lors de la créationn dde celles-ci
    print(f"saving concatene images in {temp_folder_for_concatene}")
    create_concatenate(temp_folder_for_bags, temp_folder_for_concatene)
    shutil.rmtree(temp_folder_for_bags)
    video = load_images_from_folder(temp_folder_for_concatene)
    print(f"Creating gif in {destination_path}")
    video_to_gif(video, destination_path, duration = 10)

if __name__ == "__main__":
    source_string, output_string = parser()
    source_file = Path(source_string)
    output_folder = Path(output_string)
    output_name = Path(source_string).with_suffix(".gif").name

    if source_file.suffix:
        #c'est un bag
        pass
    else:
        #c'est un dossier
        pass

    complete_process_to_be_renamed(source_file, output_folder / output_name, 25, image_reduction = 2, get_random = False)




###Notes
# Actuellement j'ouvre tous les bags en même temps, ce qui prend beaucoup de mémoire.
# Je concatene chaque première image ensemble et je la sauvegarde dans un dossier.
# Je fais pareil pour la deuxième image, etc.

# Première idée: Extraire toutes les images d'un bag, les sauvegarder dans des dossiers séparés; Je dois déjà limiter le nombre d'images.
# Ensuite je récupère les images et je les load une par une pour concaténer et réenregistrer