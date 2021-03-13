- [Twitter Real-Time Sentiment Analysis](#twitter-real-time-sentiment-analysis)
  * [Sentiment Analysis Models](#sentiment-analysis-models)
  * [Twitter API](#twitter-api)
  * [Web Server](#web-server)
  * [Twitter WebApp](#twitter-webapp)
  * [Functions](#functions)
  * [Third-Party Modules Used](#third-party-modules-used)


# Twitter Real-Time Sentiment Analysis

## Sentiment Analysis Models
Download the [dataset](https://www.kaggle.com/kazanova/sentiment140) used for the training of the Sentiment Analysis models. 

In the SentimentAnalysis directory, you can find a Jupyter-Notebook titled 'Sentiment Analysis Model' which contains the necessary pre-processing of the dataset. It then calls functions to train tweet classifiers through use of either CountVectorizer or TfidfVectorizer, while also demonstrating the functionality of some analysis functions written to understand why the model is predicting the way it is. The notebook also provides some boilerplate code to load the trained models and vectorizers for use in other cases such as our web application. 

Finally, the notebook trains a Word2Vec model and shows a demonstration of loading the model and then retrieving the most similar words (and their similarity scores) to each word in sample tweets. 

The functions called by the notebook for training the models and analyzing the predictions/words can be found in the SentimentAnalysis directory. 

---

## Twitter API
To use the twitter API functionality you must have a Twitter developer account which you can apply for [here](https://developer.twitter.com/en/apply-for-access).

Make sure to use `export BEARER_TOKEN=key` or put BEARER_TOKEN in your /etc/environment file.
If you run into issues with the web-serv container not finding your token please try running it as a root user with `sudo`.

---

## Web Server
To launch the web server you must have [docker](https://docs.docker.com/desktop/) and [docker-compose](https://docs.docker.com/compose/) installed on your machine.

Once installed, to build the containers you need to be in the root directory and type:

`docker-compose up --build`

This will intialize the docker containers and install the required python modules. Alternatively, drop the --build to open/run the containers in their current state. If you run into issues here it is typically because of an old container or conflict in the database.

In order to hop into the docker container shell yoyu can enter:

`docker exec -ti web-serv /bin/bash` in a seperate terminal. This will open bash inside the docker container where you can run some Django commands.

To make/merge changes in the database you can run:

`python manage.py makemigrations`

`python manage.py migrate`

This automatically generates the sql statements to make the changes you've made to models.py in one of the apps.

By default the web server is on port: 8000.
The website can be loaded by going to: [**http://localhost:8000/**](http://localhost:8000/)

---

## Twitter WebApp
The Twitter web app has many features such as:
- User query
- Tweet Checker
- Word Comparison
- Database Handling
- etc.

These are all on their on seperate pages on the web app and can typically be accessed with just the press of a button.
In order to use the plotly display you **must** create a plotly account and have the following as environment variables:

- PLOTLY_USER
- PLOTLY_API

Some additional functionality that can be added in the future:
- Field to customize ammount of tweets pulled
- Field to customize tweets viewed in plot


---

## Functions
To use the functions as described below, you need to obtain trained models as detailed in Sentiment Analysis. There needs to be 4 pickled files under the \Functions folder with proper names:

* count_vect_model.pickle
* count_vectorizer.pickle
* tfidf_model.pickle
* tfidf_vect.pickle

Additionally, you must have your bearer token at time of use. This is so that the user does not need to place their bearer tokens into their environment variables themselves.
### Chronological Tweets
To use this function, the user is prompted for their bearer token. It will proceed to ask for a username, verification upon Twitter server response, the quantity of tweets to pull, and which model to use. Once finished, the most positive/negative tweets aswell as all tweets occuring on most positive/negative days will be displayed along with a figure such as:

![alt text](https://github.com/whistlepark/ECE-143-Team4/blob/main/fox5sandiego.png?raw=true)

### Tweet Checker
To use this function, input your tweet and select which model to use. An example of the result is shown:

![alt text](https://github.com/whistlepark/ECE-143-Team4/blob/main/exampleTweet.png?raw=true)

##TODO: Chris, Sonya

### Word Cloud
To use this function, input a username when prompted and a word cloud of the most frequent words of the user's past 100 tweets will be displayed. The words in the word cloud are colored colored green and red for whether the word is classified as positive or negative respectively. An example word cloud is shown:

## Third-Party Modules Used
- numpy
- scikit-learn
- Django>=3.0,<4.0
- pandas
- psycopg2-binary>=2.8
- requests
- django_compressor==2.2
- django-libsass==0.7
- Pillow
- scipy
- gensim
- nltk
- plotly
- chart_studio
- seaborn
- matplotlib
- wordcloud
