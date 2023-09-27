from flask import Flask, render_template, request
from PIL import Image
from werkzeug.utils import secure_filename
import requests
from io import BytesIO
from azure.storage.blob import BlobServiceClient
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image
from PIL import Image
import numpy as np
import tensorflow as tf

app = Flask(__name__)

# Upload Folder Blob Storage Define
account_name = 'imagetemp'
account_key = 'azure__storage__account__KEY'
container_name = 'temp-image'

blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)
container_client = blob_service_client.get_container_client(container_name)
container_client2 = blob_service_client.get_container_client("model")


model_blob_client1 = container_client2.get_blob_client("vegetables.h5")
model_blob_client2 = container_client2.get_blob_client("fruits.h5")

# Get the URL of the model blob
model1_url = model_blob_client1.url
model2_url = model_blob_client2.url

# Use tf.keras.utils.get_file to load the model directly
model1_path = tf.keras.utils.get_file("vegetables.h5", model1_url, cache_dir="./")
model2_path = tf.keras.utils.get_file("fruits.h5", model2_url, cache_dir="./")

mod1 = tf.keras.models.load_model(model1_path)

mod2 = tf.keras.models.load_model(model2_path)

def pred1(mod1, img):
    labels = ['apple', 'banana', 'beetroot', 'bell pepper', 'cabbage', 'capsicum', 'carrot', 
              'cauliflower', 'chilli pepper', 'corn', 'cucumber', 'eggplant', 'garlic', 'ginger',
               'grapes', 'jalepeno', 'kiwi', 'lemon', 'lettuce', 'mango', 'onion', 'orange', 
               'paprika', 'pear', 'peas', 'pineapple', 'pomegranate','potato', 'raddish', 
               'soy beans', 'spinach', 'sweetcorn', 'sweetpotato', 'tomato', 'turnip', 'watermelon']
    img_path = img
    img = Image.open(img_path)
    img = img.resize((224, 224))
    img = image.img_to_array(img)
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    predictions = mod1.predict(img)
    res = labels[np.argmax(predictions)]
    con = round(100 * (np.max(predictions[0])), 2)
    return(res, con)

def pred2(mod2, img):
    class_names = ['Apple Braeburn', 'Apple Granny Smith', 'Apricot', 'Avocado', 'Banana', 
                   'Blueberry', 'Cactus fruit', 'Cantaloupe', 'Cherry', 'Clementine','Corn', 
                   'Cucumber Ripe', 'Grape Blue', 'Kiwi', 'Lemon', 'Limes', 'Mango', 
                   'Onion White', 'Orange', 'Papaya', 'Passion Fruit', 'Peach', 'Pear', 
                   'Pepper Green','Pepper Red', 'Pineapple', 'Plum', 'Pomegranate', 
                   'Potato Red', 'Raspberry', 'Strawberry', 'Tomato', 'Watermelon']
    img=Image.open(img)
    img = img.resize((256, 256))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    pred = mod2.predict(img_array)
    pred_class = class_names[np.argmax(pred[0])]
    confidence = round(100 * (np.max(pred[0])), 2)
    return pred_class, confidence

api_key = 'spoonacular__API__Key'
base_url = 'https://api.spoonacular.com/'

ingredients = []

@app.route('/home', methods=["GET", "POST"])
def get_img():
    return render_template('home.html')

@app.route('/display', methods=['POST'])
def upload_file():
    uploaded_files = request.files.getlist('images')
    file_paths = []
    disp_pat = []

    for uploaded_file in uploaded_files:
        if uploaded_file.filename != '':
            # Generate a unique blob name (e.g., using a UUID)
            blob_name = secure_filename(uploaded_file.filename)

            # Create a BlobClient for uploading the image
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

            # Upload the image
            blob_client.upload_blob(uploaded_file, overwrite=True)

            # Get the URL to the uploaded image
            image_urls = blob_client.url
            disp_pat.append(image_urls)
            image_url = requests.get(image_urls)
            file_paths.append(image_url)

    predictions = []

    for file_path in file_paths:
        predi1 = pred1(mod1, BytesIO(file_path.content))
        predi2 = pred2(mod1, BytesIO(file_path.content))
        thresh = 65
        if predi1[1] < thresh and predi2[1] > thresh or predi2[1] > predi1[1]:
            predictions.append(predi2)
        elif predi2[1] < thresh and predi1[1] > thresh  or predi2[1] < predi1[1]:
            predictions.append(predi1)
        elif predi2[1] == predi2[1]:
            predictions.append(predi1)
        else:
            predictions.append(('Not Identifiable', 100.00))
    for i in predictions:
        ingredients.append(i[0])
    
    return render_template('display.html', image_paths=disp_pat, predictions=predictions)

@app.route('/results')
def display_recipes():
    ingredients_str = ','.join(ingredients)

    endpoint = 'recipes/findByIngredients'
    params = {
        'apiKey': api_key,
        'ingredients': ingredients_str,
        'number': 10,  
        'instructionsRequired': 'false',  
        'ignorePantry' : 'true',
        'ranking' : 2,
    }
    
    response = requests.get(f'{base_url}{endpoint}', params=params)

    if response.status_code == 200:
        data = response.json()
        recipes = []

        for item in data:
            missed_ingredients = [ingredient['name'] for ingredient in item['missedIngredients']]
            used_ingredients = [ingredient['name'] for ingredient in item['usedIngredients']]
            recipe = {
                'title': item['title'],
                'missedIngredientCount': item['missedIngredientCount'],
                'missedIngredients' : missed_ingredients,
                'usedIngredients' : used_ingredients,
            }
            if item['missedIngredientCount'] < 5 :
                recipes.append(recipe)
        return render_template('recipe.html', recipes=recipes)
    else:
        print(f"Error: {response.status_code}")
        return render_template('error.html')

if __name__ == '__main__':
    app.run()
