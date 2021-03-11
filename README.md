- [Twitter Real-Time Sentiment Analysis](#twitter-real-time-sentiment-analysis)
  * [Sentiment Analysis Models](#sentiment-analysis-models)
  * [Twitter API](#twitter-api)
  * [Web Server](#web-server)


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
This will intialize the docker containers and install the required python modules. Alternatively, drop the --build to open/run the containers in their current state.

By default the web server is on port: 8000.
The website can be loaded by going to: [**http://localhost:8000/**](http://localhost:8000/)
