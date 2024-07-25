import matplotlib.pyplot as plt
import numpy as np
import os
import random
import tensorflow as tf
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing import image # type: ignore
import json
__class_name_to_number = {}
__class_number_to_name = {}
__model = None
food_list = ['apple_pie', 'beef_carpaccio', 'cup_cakes', 'foie_gras', 'french_fries', 'garlic_bread', 'pizza', 'spring_rolls', 'spaghetti_carbonara', 'strawberry_shortcake']
import numpy as np
from tensorflow.keras.preprocessing import image # type: ignore
import matplotlib.pyplot as plt

with open('C:\\Users\\Zaïneb\\Desktop\\food_cal\\model\\nutritional_info.json', 'r') as f:
    nutritional_info = json.load(f)
# Exemple d'informations nutritionnelles pour chaque classe
def predict_class(model, image_files, show=True):
    result = []

    # Assurez-vous que 'food_list' est défini
    food_list = list(nutritional_info.keys())
    class_name_to_number = {name: idx for idx, name in enumerate(food_list)}
    number_to_class_name = {idx: name for name, idx in class_name_to_number.items()}

    for image_file in image_files:
        img = image.load_img(image_file, target_size=(299, 299))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img /= 255.0

        # Prédisez la classe de l'image
        pred = model.predict(img)
        index = np.argmax(pred)
        predicted_class = food_list[index]

        # Obtenez les informations nutritionnelles pour la classe prédite
        nutrition = nutritional_info.get(predicted_class, {'calories par 100g(kcal)': 0, 'proteins(%)': 0, 'carbs(%)': 0, 'fats(%)': 0})

        if show:
            plt.imshow(img[0])
            plt.axis('off')
            plt.title(predicted_class)
            plt.show()

            # Créez un graphique circulaire pour les pourcentages de nutriments
            labels = ['proteins(%)', 'carbs(%)', 'fats(%)']
            sizes = [nutrition['proteins(%)'], nutrition['carbs(%)'], nutrition['fats(%)']]
            colors = ['blue', 'orange', 'green']
            explode = (0.1, 0, 0)  # "exploser" la part des protéines

            plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
            plt.axis('equal')  # Pour que le cercle soit affiché comme un cercle
            plt.title(f'Nutritional Information for {predicted_class}')
            plt.show()

        result.append({
            'classe': number_to_class_name[index],
            'nutritional_info': nutrition,
            'class_dictionary': class_name_to_number
        })

    return result


def class_number_to_name(class_num):
    return __class_number_to_name[class_num]

def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __class_name_to_number
    global __class_number_to_name

    with open("C:\\Users\\Zaïneb\\Desktop\\food_cal\\model\\class_indices.json", "r") as f:
        __class_name_to_number = json.load(f)
        __class_number_to_name = {v: k for k, v in __class_name_to_number.items()}

    global __model
    model_path = 'C:\\Users\\Zaïneb\\Desktop\\food_cal\\model\\model_trained_10class.keras'  # Remplacez par le chemin réel de votre fichier modèle
    __model = load_model(model_path)
    
    print("loading saved artifacts...done")

if __name__ == '__main__':
    load_saved_artifacts()
    images = []
    images.append('C:\\Users\\Zaïneb\\Desktop\\food_cal\\server\\test_images\\bread.jfif')
    results=predict_class(__model, images, True)
    print(results)
