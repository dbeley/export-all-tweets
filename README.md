# twitter-scripts

Some scripts using the twitter api.

The scripts need a valid config file with your twitter API keys (get them at developer.twitter.com.) in a config.ini file (see config_sample.ini for an example).

- export_all_tweets.py : Exports all tweets from one or several users in xlsx format.

## Requirements

- pandas
- tweepy

## Installation of the virtualenv with pipenv (recommended)

```
pipenv install
```

You can then launch any script with

```
pipenv run python export_all_tweets.py -h
```

## Usage

```
python export_all_tweets.py -h
```

```
usage: export_all_tweets.py [-h] [--debug] [-u USER] [-r]

Export all tweets for one or several twitter accounts.

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display debugging information.
  -u USER, --user USER  Username (separated by comma).
  -r, --export_retweets
                        Export retweets (default = False).
```
