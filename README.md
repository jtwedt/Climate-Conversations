# Climate-Conversations

Motivated by social science which shows that most Americans are concerned with but rarely talk about climate change, a small team of climate and computer scientists decided to make a game that fosters friendly conversations about historical climate events. We share how our goal of promoting civil conversations about climate change and our love for python led to the construction of our game, ‘Kitchen Table Climate Conversations.’ 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

We use Flask v0.10.1. Other versions may work, but have not been tested.

```
pip install Flask
```

See ```requirements.txt``` for other packages and versions.

### Installing

* Install prerequisites (see above).
* Download this repository and navigate to the main folder.
  * If desired, modify the data source used in $ClimateConversationsCore.py$.
* Webapp:
  * If desired, modify the port and host address of the Flask app in $play_webapp.py$ (one of the last lines).
  * Run ```python play_webapp.py```
  * Navigate to the host address.
  * (Note: this will eventually change to a much nicer config file setup!)

## Deployment

Currently, I've been running this on a free tier AWS:

1. Set up a micro EC2 instance, and open port 80 (or a port of your choosing -- change accordingly in ```play_webapp.py```).
2. Install dependencies.
3. Download this repository and navigate to the main folder.
4. Modify the port and host address of the Flask app in ```play_webapp.py```:

```    Host: 0.0.0.0```

```    Port: 80``` (or a port of your choosing, but make sure it's open on your AWS instance)

5. Open a screen with logging (```screen -L```; there is probably a better/more secure way to do this.)
6. Run $sudo python play_webapp.py$

## Running tests

This project uses ```nosetests``` and ```flask_testing``` modules.

```
pip install nosetests
pip install Flask_Testing
```

Navigate to the root of the project directory and enter ```nosetests``` to run the tests.



## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used

## Authors

See  the list of [contributors](https://github.com/jtwedt/Climate-Conversations/contributors) who participated in this project.

## Acknowledgments

* Thanks to all those who have contributed to our question database and testing. Thanks also to everyone who has patiently played our beta versions and given us feedback in formal and informal presentations of this project!
