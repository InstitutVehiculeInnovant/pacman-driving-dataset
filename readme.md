# Documentation du jeu de données de conduite

# Guide sur l'installation
Téléchargement des données.
Les différentes sources semblaient conseiller de laisser les données RAWS en ligne puis d'avoir des scripts pour télécharger.
Cela me semble adapter parce que je trouve intéressant de pouvoir télécharger les données dans des arrangements différents (trié par point ou par météo). Sauf si on arrive à faire un package qui garde ces deux informations et permet une séparation facile pour l'utilisateur. 

## Preparation
A définir

## "Requirements"
A définir


## img, from URL

<img src="https://bitbucket.org/ivi-arion/pacman-driving-dataset/raw/e66bc1afdbae3a840e1c8907b8f61a2c2a0ab905/gifs/position_trigger_02_12_2023-07_19_11_h264.gif" width="100" height= "50" />

<img src="https://bitbucket.org/ivi-arion/pacman-driving-dataset/raw/247b167dc6e6eb170ec09c5c1999440b6eb8382e/gifs/position_trigger_02_12_2023-15_36_13_h264.gif" width = "100"/>


<img src="https://bitbucket.org/ivi-arion/pacman-driving-dataset/raw/247b167dc6e6eb170ec09c5c1999440b6eb8382e/gifs/position_trigger_02_12_2023-20_00_14_h264.gif" width = "50">
|
<img src="https://bitbucket.org/ivi-arion/pacman-driving-dataset/raw/247b167dc6e6eb170ec09c5c1999440b6eb8382e/gifs/position_trigger_02_13_2023-20_43_59_h264.gif" width = "80">

## reference 
![][gif1]

<img src= [gif2] width = "80">



[gif1]: https://bitbucket.org/ivi-arion/pacman-driving-dataset/raw/e66bc1afdbae3a840e1c8907b8f61a2c2a0ab905/gifs/position_trigger_02_12_2023-07_19_11_h264.gif

[gif2]:https://bitbucket.org/ivi-arion/pacman-driving-dataset/raw/247b167dc6e6eb170ec09c5c1999440b6eb8382e/gifs/position_trigger_02_12_2023-15_36_13_h264.gif

[gif3]:https://bitbucket.org/ivi-arion/pacman-driving-dataset/raw/247b167dc6e6eb170ec09c5c1999440b6eb8382e/gifs/position_trigger_02_12_2023-20_00_14_h264.gif

[gif4]:https://bitbucket.org/ivi-arion/pacman-driving-dataset/raw/247b167dc6e6eb170ec09c5c1999440b6eb8382e/gifs/position_trigger_02_13_2023-20_43_59_h264.gif

<!-- 
## other way of writing url
![](https://bitbucket.org/ivi-arion/pacman-driving-dataset/raw/e66bc1afdbae3a840e1c8907b8f61a2c2a0ab905/gifs/position_trigger_02_12_2023-07_19_11_h264.gif)
 -->


# Description des données
Qu'est-ce que c'est un Rosbag?
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



