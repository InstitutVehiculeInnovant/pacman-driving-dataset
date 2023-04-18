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
import os
import shutil


"""
Création de gifs.

video = liste d'images

Beaucoup de process passent par des fichiers temporaires parce que je ne peux pas charger tous les bags et toutes les images dans la mémoire.
ça doit être possible d'optimiser plus en ouvrant un certain nombres de bags à la fois et en concaténant une section avant d'enregistrer.
Mais ça complexifie le code et ça n'en vaut pas la chandelle.

example of usage:
python3 gif_creator.py -i database_presentation/location3 -o images_readme/gifs -n 4 -r
python3 gif_creator.py -i database_presentation/location3 -o images_readme/gifs -n 4 -f mp4 -r

gif takes too much place, use MP4 instead.

REQUIREMENTS for optimization (commented at the end so won't be a problem if you don't have them):
pip install pygifsicle
sudo apt-get install gifsicle

"""


def get_rosbag_options(path:str, serialization_format:str="cdr"):
    storage_options = rosbag2_py.StorageOptions(uri=path, storage_id="sqlite3")
    converter_options = rosbag2_py.ConverterOptions(
    input_serialization_format=serialization_format,output_serialization_format=serialization_format)
    return storage_options, converter_options

def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', action='store', type=str, dest='output',
                        default = "images_readme/gifs", help = 'Output folder name. The name of the file will be create automatically')
    parser.add_argument('-i','--input', action='store', type=str, dest='input',
                            help = 'Input file name (bag) or folder name.',
                            default="database_presentation/location1")
    parser.add_argument('-n','--number', action='store', type=int, dest='n_bags',
                            help = 'amount of bags to open. Default = 4',
                            default = 4)
    parser.add_argument('-r', '--random', action='store_true', dest='get_random',
                            help = 'if -r, get random bags in folder', default = False)
    parser.add_argument('-d', '--divide', action='store', type=int, dest='divide',
                            help= 'Divide the number of frame by this number. Default = 1.', default = 1)
    parser.add_argument('-f', '--format', action='store', type=str, dest='format', default = "gif",
                            help = 'Format of the output file. Default = gif. Other options: mp4')
    args = parser.parse_args()
    return args.input, args.output, args.n_bags, args.get_random, args.divide, args.format

    

def bag_to_video(source_bag)->list:
    """
    Return a list of images from a bag file
    """
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

    # Enregistrement des images
        if topic == "/image_raw/compressed":
            msg_type = get_message(type_map[topic])
            msg = deserialize_message(data, msg_type)

            # Décompression de l'image compressée
            np_arr = np.frombuffer(msg.data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if img is not None:    
                frames.append(img)
            else:
                print("BUG:image non décompressée")
    
    return frames

def video_to_file(frames:list, output_file:Path, duration:int = 10, image_reduction:int = 1):
    """
    Enregistre un gif à partir d'une liste d'images.

    On sait le bag enregistré à 10 FPS
    standard duraction = 10s
    Image reduction will take 1 image every n images.
    """
    start = perf_counter() #DEBUG
    print("Starting timer for gif saving ...")
    fps = len(frames)/(duration*image_reduction)
    imageio.mimsave(output_file, frames[::image_reduction], fps = fps)

    print(f"Done saving gif in {output_file}. It took: {perf_counter() - start} s") #DEBUG


def bag_to_gif(source_bag:Path, output_file:Path, duration:int = 10, image_reduction:int = 1):
    """
    Enregistre un gif à partir d'un bag.
    """
    frames = bag_to_video(source_bag)
    print("Done reading bag. Saving file ...")
    video_to_file(frames, output_file, duration, image_reduction)


def get_bags_name_from_folder(source_folder:Path, amount_to_open: int, get_random:bool = False)->list:
    """
    Récupère les noms des n premiers bags d'un dossier. (ou aléatoirement si get_random = True)
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

    S'il en manque pour faire un carré, ajoute des carrés noirs
    """
    n_images = len(images)
    original_size = images[0].shape
    black_image = np.zeros_like(images[0])
    if n_images == 1:
        return images[0]
    elif n_images == 2:
        return cv2.hconcat(images)
    elif n_images <= 4:
        if n_images == 3: images.append(black_image)
        concat_image = cv2.vconcat([cv2.hconcat(images[:2]), cv2.hconcat(images[2:])])
    elif n_images <= 9:
        for _ in range(9-n_images): images.append(black_image)
        concat_image = cv2.vconcat([cv2.hconcat(images[:3]), cv2.hconcat(images[3:6]), cv2.hconcat(images[6:])])
    elif n_images <= 16:
        for _ in range(16-n_images): images.append(black_image)
        concat_image = cv2.vconcat([cv2.hconcat(images[:4]), cv2.hconcat(images[4:8]), cv2.hconcat(images[8:12]), cv2.hconcat(images[12:])])
    elif n_images <= 25:
        for _ in range(25-n_images): images.append(black_image)
        concat_image = cv2.vconcat([cv2.hconcat(images[:5]), cv2.hconcat(images[5:10]), cv2.hconcat(images[10:15]), cv2.hconcat(images[15:20]), cv2.hconcat(images[20:])])
    else:
        print("Too many images to concatenate. Return only with 25 images")
        return concatene_images(images[:25])
    concat_image = cv2.resize(concat_image, original_size[:2][::-1]) #Get shape and reverse it bcz cv2.resize wants the inverse of shape
    return concat_image


def extract_images_from_bag(source_bag:Path, destination_folder:Path, image_reduction:int = 1):
    """
    Extrait les images d'un bag et les enregistre dans un folder.
    Si image_reduction, on prend 1 image sur n
    """
    frames = bag_to_video(source_bag)
    if not os.path.exists(destination_folder): os.makedirs(destination_folder)
    for i, frame in enumerate(frames[::image_reduction]):
        cv2.imwrite(destination_folder.joinpath(f"{i}.jpg").as_posix(), frame)

def extract_images_from_bags(source_folder:Path, destination_folder:Path, amount_to_open:int, image_reduction:int = 1,get_random:bool = False)->list:
    """
    Extrait les images de tous les bags et les enregistre dans des folders
    """
    bags_name = get_bags_name_from_folder(source_folder, amount_to_open, get_random)
    for bag_name in bags_name:
        extract_images_from_bag(bag_name, destination_folder.joinpath(bag_name.stem), image_reduction)

def extract_images_from_multiple_folders(general_folder, i, fill):
    """
    Open one image in each folder and return a list of all of them
    """
    images = []
    black_image = None
    for image_folder in general_folder:
        image_path = image_folder.joinpath(f"{i}.jpg")
        if image_path.exists():
            if black_image is None: black_image = np.zeros_like(cv2.imread(str(image_path))) # Make a black image to fill missing images
            #Load image
            img = cv2.imread(image_path.as_posix())
            images.append(img)
        # Missing image
        else:
            if fill:
                print(f"Debug: missing image {image_path}. Fill with black image")
                images.append(black_image)
            else:
                raise Exception(f"Missing image {image_path}. Cannot create a perfect gif")
    return images

def load_concatenate_return(source_folder, fill = True):
    images_folders = [folder for folder in source_folder.iterdir()]
    n_images = len(list(images_folders[0].iterdir()))

    video =  []
    for i in range(n_images):
        images  = extract_images_from_multiple_folders(images_folders, i, fill)
        #Concatenate and return
        concat_image = concatene_images(images)
        video.append(concat_image)
    return video


def load_concatenate_save(source_folder:Path, destination_folder:Path, fill = True):
    """
    Source folder contient tous les dossiers, chaque dossier contient les images d'un bag.

    S'il manque des images dans un dossier. ça sera remplacé par un carré noir.
    """
    images_folders = [folder for folder in source_folder.iterdir()]
    n_images = len(list(images_folders[0].iterdir()))
    if not os.path.exists(destination_folder): os.makedirs(destination_folder)

    for i in range(n_images):
        images = extract_images_from_multiple_folders(images_folders, i, fill)

        #Concatenate and save 
        concat_image = concatene_images(images)
        cv2.imwrite(destination_folder.joinpath(f"{i}.jpg").as_posix(), concat_image)


def load_sorted_images_from_folder(folder:Path):
    """
    Load all images from a folder
    Images need to be named with a number
    """
    image_files = sorted(folder.glob('*.jpg'), key=lambda x: int(x.stem))
    images = []
    for filename in image_files:
        img = cv2.imread(filename.as_posix())
        if img is not None:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            images.append(img_rgb)
        else:
            print(f"Debug: {filename} is not an image. It should'nt happen") 
    return images

def folder_to_gif(source_folder, destination_path, amount_to_open, image_reduction:int = 1, get_random:bool = False, ):
    temp_folder = Path("Temp")
    temp_folder_for_bags = temp_folder.joinpath("bags")
    temp_folder_for_concatene = temp_folder.joinpath("concatene")
    if os.path.exists(temp_folder): shutil.rmtree(temp_folder) # Clean temp before creating new one to remove left overs
    
    extract_images_from_bags(source_folder, temp_folder_for_bags, amount_to_open, image_reduction, get_random) #Reduction d'images lors de la créationn dde celles-ci
    print(f"saving concatene images in {temp_folder_for_concatene}")
    
    #SOL 1: Save concatene images #Il n'y a que 50 images à enregistrer et reload. ça fait pas beaucoup de temps ni de place finalement. Les deux sols sont bonnes
    # load_concatenate_save(temp_folder_for_bags, temp_folder_for_concatene)
    # shutil.rmtree(temp_folder_for_bags) 
    # video = load_sorted_images_from_folder(temp_folder_for_concatene)
    
    #SOL 2: don't save concatenate images, keep them in memory to save time
    video = load_concatenate_return(temp_folder_for_bags)
    shutil.rmtree(temp_folder_for_bags) 
    
    print(f"Creating gif in {destination_path}")
    video_to_file(video, destination_path, duration = 10)
    shutil.rmtree(temp_folder)

if __name__ == "__main__":
    source_string, output_string, amount_to_open, get_random, image_reduction, format = parser()
    source_file = Path(source_string)
    output_folder = Path(output_string)
    if format == "gif":
        output_file = output_folder.joinpath(source_file.name).with_suffix(".gif")
    elif format == "mp4":
        output_file = output_folder.joinpath(source_file.name).with_suffix(".mp4")
    else:
        raise Exception(f"Format {format} not supported")

    if not source_file.exists():
        raise Exception(f"{source_file} doesn't exist")

    if source_file.suffix:
        #c'est un bag
        bag_to_gif(source_file, output_file, image_reduction = image_reduction)
    else:
        #c'est un dossier
        folder_to_gif(source_file, output_file, amount_to_open = amount_to_open, image_reduction = image_reduction, get_random = get_random)
        
    #optimizing the gif
    # if format == "gif":
    #     from pygifsicle import optimize
    #     print("Optimizing gif...")
    #     optimize(output_file, output_file.with_suffix("_optimized.gif"))
    #     print("Done")