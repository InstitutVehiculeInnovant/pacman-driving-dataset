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

## Liste des topics enregistrés

`Nom du topic`:
Type de message Ros
unité
courte description

`/bboxs`: 
Type: Vision_msgs/msg/Detection2DArray
Unité: 
Description: 

`/camera_info`: 
Type:
Unité: 
Description: 

`/can/abs`: 
Type:
Unité: 
Description: 

`/can/accel_lat`: 
Type:
Unité: 
Description: 

`/can/accel_long`: 
Type:
Unité: 
Description: 

`/can/accel_pedal_pos`: 
Type:
Unité: 
Description: 

`/can/accel_vert`: 
Type:
Unité: 
Description: 

`/can/brake_pressure`: 
Type:
Unité: 
Description: 

`/can/speed1`: 
Type:
Unité: 
Description: 

`/can/steer_col_tq`: 
Type:
Unité: 
Description: 

`/can/steering_angle`: 
Type:
Unité: 
Description: 

`/can/traction`: 
Type:
Unité: 
Description: 

`/can/wheel_fl_speed`: 
Type:
Unité: 
Description: 

`/can/wheel_fr_speed`: 
Type:
Unité: 
Description: 

`/can/wheel_rl_speed`: 
Type:
Unité: 
Description: 

`/can/wheel_rr_speed`: 
Type:
Unité: 
Description: 

Type:
Unité: 
Description: 
`/fix`: 
Type:
Unité: 
Description: 

`/fix_velocity`: 
Type:
Unité: 
Description: 

`/heading`: 
Type:
Unité: 
Description: 

`/image_raw/compressed`: 
Type:
Unité: 
Description: 

`/imu/data`: 
Type:
Unité: 
Description: 

`/live_tracker`: 
Type:
Unité: 
Description: 

`/obj_centers`: 
Type:
Unité: 
Description: 

`/parameter_events`: 
Type:
Unité: 
Description: 

`/rosout`: 
Type:
Unité: 
Description: 

`/tracked_objects`: 
Type:
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
    - bag:
      ...
- position:
    ...
```

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



