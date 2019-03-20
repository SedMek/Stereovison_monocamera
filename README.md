# Stereovison_monocamera

Ce projet permet de générer des cartes de profondeur à partir d'images successives de colis se déplaçant sur un tapis.

-------------------------------

## Instructions d'installation sous Windows: 

* Installer pytorch (via anaconda)
* python3 -m pip install -r requirements.txt

-------------------------------

## Comment le tester: 
Pour lancer un test, exécuter la commande suivante en remplaçant "yourpath" par votre path contenant le dossier Depthnet:
```
python3 run_inference.py --output-raw --output-depth --no-resize --dataset-dir yourpath\DepthNet\test_data\full_size --pretrained yourpath\Depthnet\training_results\512_progressive_64_to_512\checkpoint.pth.tar  --output-dir yourpath\DepthNet\output_512_progressive\full_size --frame-shift 3
```
--dataset-dir : le dossier contenant les images à tester <br>
--output-dir : le dossier qui contiendra les outputs images et npys, il est créé s'il n'existe pas <br>
--frame-shift : vaut 1 pour faire déduire le depth map de 2 photos, vaut 2 pour déduire le depthmap de 3 photos ... <br>
--pretrained : fait référence aux résultats des entraînement que nous avons effectués. Il y a deux versions : <br>
* Le fichier checkpoint.pth.tar qui est contenu dans 512_progressive_64_to_512 
* Le fichier checkpoint.pth.tar qui est contenu dans 512_finetuned_from_stillbox <br>

--output-raw : si cet argument est ajouté, un fichier npy de la carte de profondeur est généré <br>
--output-depth : si cet argument est ajouté, l'image de plot de la carte de profondeur est généré <br>

--------------------------------

## Comment l'entraîner:

Pour effectuer le training il faut lancer la commande suivante :
```
python3 train.py -j8 --lr 0.01 path/vers/datasets/ --log-output --activation-function elu --bn
```

Pour faire un training sur une résolution spécifique il faut découper les images. Le fichier `dataloader.py` du dossier **data_processing** prend en paramètre le path du dossier datasets, le numéro du scénario (en supposant que les scénarios ont les noms scenario_0, scenario_1 ... ) et le nombre des images à cropper présentes dans le dossier. 

Ensuite, il faut générer le fichier `metadata.json` pour paramétrer l'apprentissage. Pour générer ce fichier, il faut ouvrir le fichier `metadata_generator.py` du dossier **data_processing**, modifier le path et mettre le path du dossier qui contient les images et les npy, ouvrir une invite de commande dans le répertoire du fichier `metadata_generator.py` et lancer la commande:
```
python3 metadata_generator.py --sc 10 --s resolution
``` 
(En remplaçant résolution par : 64, 128, 256 ou 512).
Un fichier `metadata.json` est alors généré dans le dossier du `metadata_generator.py`, il faut le déplacer dans le dossier contenant images et npy.

Le dossier **datasets** doit contenir des sous dossiers, chacun d'eux avec :
* Les images
* Les fichiers npy
* Le fichier metadata.json

Une fois la commande exécutée, l'entraînement est lancé sur tous les sous dossiers.

Pour entraîner à partir d'un modèle pré-entraîné il faut ajouter l'argument --pretrained /path/modèle_préentraîné. 

-------------------------------

## Résultats d'entraînements, stockés dans le dossier "training results" : 
* 512_progressive_64_to_512 : il correspond à un entraînement progressif sur les images Solystic de 64 puis 128 puis 256 puis 512, en commençant par un résultat préentraîné de Stillbox en résolution 64.
* 512_finetuned_from_stillbox : il correspond à un finetuning du Stillbox 512 avec des images Solystic 512

-------------------------------

## Quelques examples des résultats, contenus dans le dossier "Ressources/Examples":
* Groundtruth: données originales
* test_512_progressive_64_to_512 : résultat du test avec l'entraînement 512_progressive_64_to_512
* test_512_finetuned_from_stillbox : résultat du test avec l'entraînement 512_finetuned_from_stillbox
