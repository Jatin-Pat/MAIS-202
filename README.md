# Financial News Sentiment Analysis
Final project for McGill AI Society Intro to ML Bootcamp (2022).

Training data from [Hugging Face](https://huggingface.co/datasets/financial_phrasebank)

## Project description
This project sets out to predict the sentiment in financial news reports to gauge analysts' perceptions about a publicly traded company. I implemented the Naive Bayes classifier model using Scikit-Learn, and named-entity recognition (NER) using the Spacy library. The web app was built using Flask. 

## Running the app
In order to run the web app and test the classifier, install the packages in requirements.txt and download files from this repo. Then, change into app.py and run the following in the terminal
```
 python app.py
```
Lastly, open a browser and navigate to your [localhost](http://localhost:5000/)

## Repository organization
1. Deliverable/
    * Progress logs submitted to the Bootcamp technical project managers
3. static/
  * CSS files for web app
4. templates/
 * HTML templates for web app
5. model.py
 * Python script containing final model
6. app.py
 * Main script to instantiate server (on localhost)
7. data.csv
 * Dataset used for model training
