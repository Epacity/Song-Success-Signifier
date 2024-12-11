# Song Success Signifier 
### Final Project for Data Management for Data Science (01:198:210)
### Net IDs: jca159, bg592, anm212

This project predicts which genres a song will do the best in given its lyrics and a one-word theme. The theme is generated with OpenAI's GPT 4.0 Mini based on the song's lyrics.

The project is split into two parts: the scraper and the model. The scraper pulls song information (~2400 songs) from Spotify across 18 different genres, and the model uses this information to predict which genres work best for song lyrics that a user inputs. The scraped songs are stored in a local MongoDB database.

---

## Setup Instructions
### General Setup
To isolate project dependencies, create a virtual environment:
```
python3 -m venv venv
```
Activate the virtual environment with the following command:
```
source ./venv/bin/activate
```
Install all necessary libraries by running:
```
pip install -r requirements.txt
```
### MongoDB Setup
Make sure MongoDB is intalled and running on your computer. You can do so by following the instructions on the Mongo website:
https://www.mongodb.com/docs/manual/installation/

### Scraper Setup
There are two third-party services that the scraper depends on: 2Captcha for solving the reCaptcha v3 for Spotify's login and OpenAI for generating the one-word topics for each song.

First, go to https://2captcha.com/ and sign into your account. If you don't have an account, you'll have to create one and load funds to use the autonomous captcha solving. After logging in, copy your API key on the home page and either set an environment variable `TWOCAP_KEY` to the key, or set the constant `TWOCAP_KEY` in `scraper/config.py` to the key.

Next, head to https://platform.openai.com/ and sign into / create an account. You'll need to load funds to generate one-word song topics. There are three pieces of information you'll need: your organization ID, your project ID, and a secret API key for your project. To get your organization ID, go to `Organization > General`. To get your project ID, go to `Project > General`. To create a secret key, go to `Project > API keys` and follow the instructions.

You can either set these environment variables: `OPENAI_ORGANIZATION_ID` for organization ID, `OPENAI_PROJECT_ID` for project ID, and `OPENAI_API_KEY` for the secret key OR navigate to `scraper/topic_classifier.py` and change the arguments for the OpenAI client object.

Finally, change the placeholder account credentials to those of your Spotify account in the `SPOTIFY_ACCOUNT` tuple of `scraper/config.py`.

---
## Running the Scraper
Make sure your Mongo server is running locally on port `27017`. Then, run this command:
```
python3 scraper/main.py
```
This will take ~30 minutes to run until completion. You can toggle the variable `CLEAR_DATABASE_ON_RESTART` in `scraper/config.py` to reset the MongoDB database on each run of the scraper.

## Running the Model
Find song lyrics that you want to analyze and put them into `lyrics.txt`. Then, run this command:
```
python3 model/main.py
```
The output should look something like this:
```
Getting songs DataFrame from MongoDB...
Training the model...
Pulling the test song lyrics from lyrics.txt...
Generating topic from the song lyrics...
Song topic: Embarrassment
Predicting the success of a sample song...
Here are the probabilities of this song's success in each genre:
Funk: 14.00%
K-Pop: 47.00%
Folk/Americana: 41.00%
Reggaeton: 3.00%
Indie: 32.00%
Pop: 71.00%
Latin: 22.00%
Kids: 6.00%
Hip-Hop: 22.00%
R&B: 42.00%
Jazz: 40.62%
Blues: 10.00%
Country: 61.00%
Metal: 31.00%
Christian/Gospel: 46.28%
Rock: 53.73%
Dance/Electronic: 42.00%
Showing model visualizations...
Done!
```
