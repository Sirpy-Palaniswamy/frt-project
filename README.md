<h1>Recipe Generator</h1>
<h2>Overview</h2>
This web application is designed to simplify the process of identifying ingredients in images and provide recipe recommendations based on those ingredients. It's built using the Flask web framework in Python and integrates with the Spoonacular API to offer a comprehensive cooking and meal planning experience. Currently the application is only at the skeleton state, further development on the user experience will be done with more given time in the future. The application is currently a MVP application only.
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
<h2>Dependencies</h2>
This application relies on several key dependencies, including:
<ul>
    <li>Flask: The web framework used for building the application.</li>
    <li>TensorFlow: For running machine learning models.</li>
    <li>Pillow: For image processing and handling.</li>
    <li>Azure Blob Storage SDK: If Azure Blob Storage is used for image storage.</li>
</ul>
Please refer to the requirements.txt file for a complete list of dependencies and versions.
<hr>
<h2>Future Scope:</h2>
<ul>
  <li>The application is only done as a MVP product, so the plan to develop more user interface will be done with the help of user experience comments in the future.</li>
  <li>The project as of now is able to only able to predict images of single ingredient, further scope includes the multi segement image classification to classify the image of a cluster of ingredients</li>
  <li>The trained models are for common vegetables and fruits available to the general, further improvement on more region specifc ingrredients such as cassava, various types of meat, etc,.</li>
  <li>The results as of now only display recipe names, maybe in future, we can define a model to generate recipe based on the recipe given to it.</li>
  <li>The usage of the web app might be inconvenient for a lot, but in future might move on to android and iOS platforms</li>
</ul>
<hr>
<h2>Screen Shots</h2>
<h3>Azure Storage Service</h3>
<h4>Used Containers List</h4>
<img src="https://github.com/Sirpy-Palaniswamy/frt-project/blob/main/screenshots/Storage_Containers.png" />
<h4>Container 1 (For Model Storage)</h4>
<img src="https://github.com/Sirpy-Palaniswamy/frt-project/blob/main/screenshots/Storage_Model_Container.png"/>
<h4>Container 2 (For Image Storage)</h4>
<img src="https://github.com/Sirpy-Palaniswamy/frt-project/blob/main/screenshots/Storage_Image_Container.png"/>
<h3>Azure App Services</h3>
<h4>Azure App Deployed Page</h4>
<img src="https://github.com/Sirpy-Palaniswamy/frt-project/blob/main/screenshots/Azure_App_Service.png">
<h3>Model Summary</h3>
<h4>Model 1</h4>
<a href="https://github.com/Sirpy-Palaniswamy/frt-project/blob/main/screenshots/vegetable_model.png">MODEL 1, click to view</a>
<h4>Model 2</h4>
<a href="https://github.com/Sirpy-Palaniswamy/frt-project/blob/main/screenshots/fruits_model.png">MODEL 2, click to view</a>
<h2>References:</h2>
<ul>
  <li>https://spoonacular.com/food-api/docs#Search-Recipes-by-Ingredients</li>
  <li>https://www.kaggle.com/datasets/sshikamaru/fruit-recognition</li>
  <li>https://www.kaggle.com/datasets/kritikseth/fruit-and-vegetable-image-recognition</li>
</ul>
<h2>Author</h2>
<h3>
    Sirpy Palaniswamy
</h3>
<h3>
    GitHub: [https://github.com/Sirpy-Palaniswamy]
</h3>
