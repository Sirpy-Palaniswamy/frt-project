<h1>Recipe Generator</h1>
<h2>Overview</h2>
This web application is designed to simplify the process of identifying ingredients in images and provide recipe recommendations based on those ingredients. It's built using the Flask web framework in Python and integrates with the Spoonacular API to offer a comprehensive cooking and meal planning experience.
<hr>
<h2>Tech Stack</h2>
<ul>
    <h3><bold>1. Softwares Used</bold></h3>
  <ul>
    <li>Visual Studio Code</li>
    <li>Azure CLI</li>
    <li>Azure Services</li>
    <li>GitHub</li>
    <li>Git-Scm</li>
  </ul>
  <h3><bold>2. Frameworks Used</bold></h3>
  <ul>
    <li>Python - 3.8.x</li>
    <li>Flask</li>
    <li>Tensorflow - 2.13.0</li>
    <li>Numpy</li>
    <li>HTML / CSS</li>
  </ul>
</ul>
<hr>
<h2>Key Features</h2>
<ul>
  <li><h3>Ingredient Recognition</h3>The application uses two machine learning models trained on datasets sourced from kaggle. These models are trained and excelled in recognizing various fruits and vegetables from the given image</li>
  <li><h3>API Integration</h3>Using the Spoonacular API available to the public, we integrate the <i><bold>findByIngredients</bold></i> api call. With the predictions made by the model from the images, the list of ingredients is sent over to the API, the response is then gathered from the call made and displayed onto the application. Spoonacular API also has the feature of returning the <i>"missedIngredients"</i> and <i>"usedIngredients"</i> from the recipes displayed, which helps the user to understand what is required for the recipe and what's not.</li>
  <li><h3>User Interface</h3>The application runs on a minimal design for now, with the ability of the user to upload all the images of the ingredients he has at hand to the application. After prediction, the user is able to view the possible recipes on the application with the details of the recipe ingredients required possibly if missing any.</li>
</ul>
<hr>
<h2>Working</h2>
<ul>
  <li>Two models, one for fruits and another for vegetables was custom trained on the dataset sourced from kaggle. The models were then saved on to the Azure Storage for the application to access the model during the period of predicition analysis</li>
  <li>Next, a flask application was developed using Visual Studio Code and the Python 3.8.x interpreter.</li>
  <li>The Spoonacular API was then integrated along with the Azure Storage Client Integration with the application.</li>
  <li>The first page is the display of the feature of uploading the user's image on to the application, the user selects multiple various ingredients onto the application. The application then sends these images to the Azure Storage for access during the prediction analysis period.</li>
  <li>Once the images have been finished uploading, the models saved in the Azure Storage are then accessed by the application to predict the user's images submitted, and a display of the images submitted and the prediction of the image along with it is displayed for the user's confirmation.</li>
  <li>Upon confirming to produce recipes, the Spoonacular API is called to gather recipes based on the ingredient predictions made in the previous step. The Spoonacular API call has been tuned to proudce 10 recipes and also to only display recipes that are missing a maximum of 5 ingredients from the given ingredient lists (this is expandable in the future)</li>
  <li>The response from the API is then displayed on the results page of the application.</li>
  <li>With the name of the recipe, the user is able to search online to find out the cooking method for the same.</li>
</ul>
<hr>
<h2>Future Scope:</h2>
<ul>
  <li>The project as of now is able to only able to predict images of single ingredient, further scope includes the multi segement image classification to classify the image of a cluster of ingredients</li>
  <li>The trained models are for common vegetables and fruits available to the general, further improvement on more region specifc ingrredients such as cassava, various types of meat, etc,.</li>
  <li>The results as of now only display recipe names, maybe in future, we can define a model to generate recipe based on the recipe given to it.</li>
  <li>The usage of the web app might be inconvenient for a lot, but in future might move on to android and iOS platforms</li>
</ul>
<hr>
<h2>Screen Shots</h2>
<h4>Azure Storage Service</h4>
![alt text](https://github.com/Sirpy-Palaniswamy/frt-project/blob/main/screenshots/Storage_Containers.png)
<h2>References:</h2>
<ul>
  <li>https://spoonacular.com/food-api/docs#Search-Recipes-by-Ingredients</li>
  <li>https://www.kaggle.com/datasets/sshikamaru/fruit-recognition</li>
  <li>https://www.kaggle.com/datasets/kritikseth/fruit-and-vegetable-image-recognition</li>
</ul>
