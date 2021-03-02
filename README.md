- [Twitter Real-Time Sentiment Analysis](#twitter-real-time-sentiment-analysis)
  * [Twitter API](#twitter-api)
  * [Web Server](#web-server)


# Twitter Real-Time Sentiment Analysis

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
