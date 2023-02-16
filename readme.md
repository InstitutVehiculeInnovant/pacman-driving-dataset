# Documentation du jeu de données de conduite

# Guide sur l'installation
Téléchargement des données.
Les différentes sources semblaient conseiller de laisser les données RAWS en ligne puis d'avoir des scripts pour télécharger.
Cela me semble adapter parce que je trouve intéressant de pouvoir télécharger les données dans des arrangements différents (trié par point ou par météo). Sauf si on arrive à faire un package qui garde ces deux informations et permet une séparation facile pour l'utilisateur. 

## Preparation
A définir

## "Requirements"
A définir


<!-- <img src="https://bitbucket.org/ivi-arion/pacman-driving-dataset/raw/e66bc1afdbae3a840e1c8907b8f61a2c2a0ab905/gifs/position_trigger_02_12_2023-07_19_11_h264.gif"> -->

## visualisation

|![][gif1] | ![][gif2] |
|----------|-----------|
|![][gif3] | ![][gif4] |

[gif1]:https://bitbucket.org/ivi-arion/pacman-driving-dataset/raw/71eb4baa7f09b937749f95a6470cbb22a9652244/gifs_loc2/position_trigger_02_09_2023-21_44_29_h264.gif
[gif2]:https://bitbucket.org/ivi-arion/pacman-driving-dataset/raw/71eb4baa7f09b937749f95a6470cbb22a9652244/gifs_loc2/position_trigger_02_10_2023-08_48_34_h264.gif
[gif3]:https://bitbucket.org/ivi-arion/pacman-driving-dataset/raw/71eb4baa7f09b937749f95a6470cbb22a9652244/gifs_loc2/position_trigger_02_11_2023-07_50_45_h264.gif
[gif4]:https://bitbucket.org/ivi-arion/pacman-driving-dataset/raw/71eb4baa7f09b937749f95a6470cbb22a9652244/gifs_loc2/position_trigger_02_11_2023-12_21_48_h264.gif






# Description des données
## ROS - Robot Operating System
ROS est un ensemble de librairies et d'outils qui permettent de fabriquer une application de robotique. L'architecture ROS permet une communication simple entre différents éléments via la publication de messages vers des topics. 
Pour recevoir un message, un élément doit *s'abonner* à /écouter un topic. Pour envoyer, il suffit de *publier* à cette adresse.

Un **ROSbag** est un enregistrement des messages reçu par un ou plusieurs *topics*. 
La structure d'un message est semblable à celle d'un JSON, c'est à dire qu'il y a des objets qui possèdent des valeurs et des listes. 

## Liste des topics enregistrés
__Notes__: Je pensais que la detection ne serait pas dans la database qu'on publie? *bbox, live_tracker, tracked_object, object_centers*


`Nom du topic`:
Type de message Ros
unité si applicable
courte description

`/bboxs`: 
Type: vision_msgs/msg/Detection2DArray
Description: En cas de de détection d'objet, la position de la bouding box ainsi que l'identifiant du type d'objet détecté sera disponible dans detections.bbox.

`/camera_info`: 
Type: sensor_msgs/msg/CameraInfo
Description: **A completer** Probablement la calibration de la camera?

`/can/abs`: 
Type: std_msgs/msg/Bool
Unité: booléen
Description: True lorsque l'ABS du vehicule est active, pas de messages le reste du temps. Le topic peut rester vide sur un bag complet.

`/can/accel_lat`: 
Type: std_msgs/msg/Float32
Unité: m/s²
Description: Accélération latérale ressentie par les occupants du véhicule. Une valeur positive représente une accélération vers la droite, en général parce que le véhicule tourne vers la gauche.
Une valeur négative est une accélération vers la gauche.

`/can/accel_long`: 
Type: std_msgs/msg/Float32
Unité: m/s²
Description: Accélération longitudinale ressentie par les occupants du véhicule. Une valeur positive représente une accélération du véhicule, les occupants sont pressés contre leur siège, le véhicule accélère les occupants vers l'avant. 
Une valeur négative correspond à un freinage du véhicule et les occupants gardent leur inertie et peuvent être penché vers l'avant du véhicule.

`/can/accel_pedal_pos`: 
Type: std_msgs/msg/Float32
Unité: Pas d'unités, range [0,102.3]
Description: Accélération de la pédale conducteur transmise au véhicule. En cas de cruise control, la valeur correspond à celle donnée par le cruise control. 

`/can/accel_vert`: 
Type: std_msgs/msg/Float32
Unité: m/s²
Description: Acceleration verticale. Dans la majorité des cas, elle correspond simplement à l'accélération gravitationnelle.  

`/can/brake_pressure`: 
Type: std_msgs/msg/UInt16
Unité: Pas d'unité, range [0,65535] **Quel est la valeur maximale observée dans les données?**
Description: **pas sûr si c'est la valeur de la pedale ou une valeur dépendante d'autres paramètres non identifiés**

`/can/speed1`: 
Type: std_msgs/msg/Float32
Unité: km/h 
Description: Vitesse du véhicule

`/can/steer_col_tq`: 
Type: std_msgs/msg/Float32
Unité: **unite?** range [-8,8]
Description: *Force appliquée au volant* **pas clair non plus**

`/can/steering_angle`: 
Type: std_msgs/msg/Float32
Unité: **Unite?** range [-4876.8,1676.7]
Description: Position du volant. Negatif: tournant vers la droite. Positif: tournant vers la gauche

`/can/traction`:  **Donnees?**
Type: std_msgs/msg/Bool
Unité: 
Description: 

`/can/wheel_fl_speed`: 
Type: std_msgs/msg/Float32
Unité: rad/s
Description: Vitesse de la roue avant gauche.

`/can/wheel_fr_speed`: 
Type: std_msgs/msg/Float32
Unité: rad/s
Description: Vitesse de la roue avant droite.

`/can/wheel_rl_speed`: 
Type: std_msgs/msg/Float32
Unité: rad/s
Description: Vitesse de la roue arrière gauche.

`/can/wheel_rr_speed`: 
Type: std_msgs/msg/Float32
Unité: rad/s
Description: Vitesse de la roue arrière droite.

`/fix`: 
Type: sensor_msgs/msg/NavSatFix
Description: Position *GPS* du véhicule. 

`/fix_velocity`: 
Type: geometry_msgs/msg/TwistWithCovarianceStamped
Unité: m/s
Description: Vitesse du véhicule **est-ce que X et Y sont basé sur le repère de la voiture ou longitude/latitude?**

`/heading`: 
Type: sensor_msgs/msg/Imu
Description: Direction du véhicule. Format Quaternion (w,x,y,z). Pour obtenir une orientation en °:
`heading = -atan2(2*(w*z + x*y), 1-2*(y**2 + z**2)) * 180 / PI`
**angles de mémoire**
Est: 0
Nord: 90
Sud: -90
Ouest: +-180

`/image_raw/compressed`: 
Type: sensor_msgs/msg/CompressedImage
Format: JPEG
Description: Image de la route

`/imu/data`:  **Pas de données**
Type: sensor_msgs/msg/Imu
Unité: 
Description: 

`/live_tracker`: **Meme chose que bbox?**
Type: vision_msgs/msg/Detection2DArray
Unité: 
Description: 

`/obj_centers`: 
Type: vision_msgs/msg/Detection2D
Unité: 
Description: 

`/parameter_events`: 
Type: rcl_interfaces/msg/ParameterEvent
Unité: 
Description: Présent par défaut

`/rosout`: 
Type: rcl_interfaces/msg/Log
Unité: NA
Description: Logs, présent par défaut 

`/tracked_objects`: 
Type: vision_msgs/msg/Detection2DArray
Unité: 
Description: 






C'est quoi un topic?

Liste des topics:
Unités et signification de chacun, ce qu'il peut contenir. La fréquence





## Structure des documents

Quatres dossiers séparent le type de route. Ensuite chaque sous-dossier contient tous les bags associés à une position.
Un YAML global référence tous les bags avec leur date, et la météo. (copie en json pour avoir un avis du MTQ sur leurs préférences)

    .
    ├── position1
    │   ├── position_trigger1.bag
    │   │   ├── metadata.yaml
    │   │   └── position_trigger1.bag_0.db3
    │   ├── position_trigger2.bag
    │   ├── ...
    │   ├── informations.json
    │   └── informations.yaml
    ├── position2
    └── ...

Les "metadata.yaml" sont déjà présents dans la base de données et contiennent les infos relatives à chaque bag.

*Strucutre d'informations.yaml:*
```yaml
- position:
  nom_folder: "position1"
  localisation : (-73,45)
  nombre_de_bags: 17
  bags:
    - bag:
      name: "nomDuBag.bag"
      weathercode: 75
      meteo:  soleil
      timestamp: 2022_01_27-10h00 (format exemple)
      type: Intersection
      essui-glace: true
      abs: false
    - bag:
      ...
- position:
    ...
```

**Ajouter ABS dans le code**

Si la meteo n'est pas disponible dans la base de données (pour n'importe quelle raison), la valeur sera -1

Les directions ne sont pas séparées, ainsi on pourra trouver facilement toutes les manières de prendre une même intersection.



## Génération des données


EN: (
For the driving videos, sample points were chosen on specific type of roads:
-Straight roads
-Curvy roads
-intersection between two roads
-Starting/exit of highway

Multiple cars were equiped with gps to trigger when they passed through these points.)



# License

# Citations

# Travail additionnel
(si on veut citer les autres travaux de IVIS)



