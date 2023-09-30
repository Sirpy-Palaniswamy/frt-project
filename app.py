from flask import Flask, render_template, request, redirect, url_for
from PIL import Image, UnidentifiedImageError
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
account_key = 'your_azure_atorage_api_key'
container_name = 'temp-image'

blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)
container_client = blob_service_client.get_container_client(container_name)
container_client2 = blob_service_client.get_container_client("model")


model_blob_client1 = container_client2.get_blob_client("ingre.h5")

# Get the URL of the model blob
model1_url = model_blob_client1.url

# Use tf.keras.utils.get_file to load the model directly
model1_path = tf.keras.utils.get_file("ingre.h5", model1_url, cache_dir="./")

mod1 = tf.keras.models.load_model(model1_path)

def pred1(mod1, img):
    labels = ['apple', 'banana', 'beetroot', 'bell pepper', 'cabbage', 'capsicum', 'carrot', 
              'cauliflower', 'chilli pepper', 'corn', 'cucumber', 'eggplant', 'garlic', 'ginger',
               'grapes', 'jalepeno', 'kiwi', 'lemon', 'lettuce', 'mango', 'onion', 'orange', 
               'paprika', 'pear', 'peas', 'pineapple', 'pomegranate','potato', 'raddish', 
               'soy beans', 'spinach', 'sweetcorn', 'sweetpotato', 'tomato', 'turnip', 'watermelon']
    img_path = img
    try:
        img = Image.open(img_path)
    # Process the image here
    except UnidentifiedImageError as e:
        print(f"Error: {e}"), 400
    #img = Image.open(img_path)
    img = img.resize((224, 224))
    img = image.img_to_array(img)
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    predictions = mod1.predict(img)
    res = labels[np.argmax(predictions)]
    con = round(100 * (np.max(predictions[0])), 2)
    return(res, con)

api_key = 'spoonacular_api'
base_url = 'https://api.spoonacular.com/'

ingredients = []

ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/home', methods=["GET", "POST"])
def get_img():
    return render_template('home.html')

@app.route('/display', methods=['POST'])
def upload_file():
    if 'images' not in request.files:
        # Handle case where no file is selected
        return "No file selected", 400
    else:
        uploaded_files = request.files.getlist('images')
    
    file_paths = []
    disp_pat = []

    for uploaded_file in uploaded_files:
        if uploaded_file.filename != '' and allowed_file(uploaded_file.filename):
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
        else:
            return f'<script>alert("Invalid file. Only JPG, JPEG are allowed"); window.location.replace("{url_for("get_img")}");</script>'


    predictions = []

    for file_path in file_paths:
        predi1 = pred1(mod1, BytesIO(file_path.content))
        thresh = 65
        if predi1[1] > thresh:
            predictions.append(predi1)
        else:
            predictions.append(('This image is probably not a Fruit or Vegetable', 100.00))
    for i in predictions:
        ingredients.append(i[0])
    print(BytesIO(file_path.content))
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
