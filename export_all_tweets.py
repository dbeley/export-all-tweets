import configparser
import pandas as pd
import argparse
from pathlib import Path
import logging
import time
import tweepy

logger = logging.getLogger()
temps_debut = time.time()
config = configparser.ConfigParser()
config.read("config.ini")


def twitterconnect():
    ConsumerKey = config["twitter"]["ConsumerKey"]
    SecretKey = config["twitter"]["SecretKey"]
    AccessToken = config["twitter"]["AccessToken"]
    AccessTokenSecret = config["twitter"]["AccessTokenSecret"]

    auth = tweepy.OAuthHandler(ConsumerKey, SecretKey)
    auth.set_access_token(AccessToken, AccessTokenSecret)
    return tweepy.API(auth)


def process_status(status):
    tweet = {}
    tweet["text"] = status.full_text
    tweet["retweets"] = status.retweet_count
    tweet["favorites"] = status.favorite_count
    tweet["source"] = status.source
    tweet["date"] = status.created_at
    tweet["geo"] = status.geo
    tweet["name"] = status.user.name
    tweet["screen_name"] = status.user.screen_name
    tweet[
        "url"
    ] = f"https://twitter.com/{tweet['screen_name']}/status/{status.id}"
    # try:
    #     tweet["hashtags"] = status.entities["hashtags"]
    # except Exception as e:
    #     print(e)
    try:
        tweet["media"] = status.entities["media"][0]["media_url_https"]
    except Exception as e:
        logger.debug(e)
    return tweet


def main():
    args = parse_args()
    list_users = [x.strip() for x in args.user.split(",")]
    api = twitterconnect()
    tweets = []
    Path("Exports").mkdir(parents=True, exist_ok=True)

    for user in list_users:
        for index, status in enumerate(
            tweepy.Cursor(
                api.user_timeline, id=user, tweet_mode="extended"
            ).items(),
            1,
        ):
            logger.info("Extracting tweet %s for %s.", index, user)
            if args.export_retweets:
                tweets.append(process_status(status))
            else:
                # If not retweet
                if not status.full_text.lower().startswith("rt @"):
                    tweets.append(process_status(status))
                else:
                    logger.info("Status is a retweet. Skipping.")

        df = pd.DataFrame.from_records(tweets)
        print(df.head())

        writer = pd.ExcelWriter("Exports/export_" + str(user) + ".xlsx")
        df.to_excel(writer, "Sheet1", index=False)

        writer.save()

        # problem with tweet text
        # df.to_csv("export_" + str(user) + ".csv", sep="\t", index=False)
    logger.info("Runtime : %.2f seconds." % (time.time() - temps_debut))


def parse_args():
    format = "%(levelname)s :: %(message)s"
    parser = argparse.ArgumentParser(
        description="Export all tweets for one or several twitter accounts."
    )
    parser.add_argument(
        "--debug",
        help="Display debugging information.",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
    )
    parser.add_argument(
        "-u", "--user", type=str, help="Username (separated by comma)."
    )
    parser.add_argument(
        "-r",
        "--export_retweets",
        help="Export retweets (default = False).",
        dest="export_retweets",
        action="store_true",
    )
    parser.set_defaults(export_retweets=False)

    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel, format=format)
    return args


if __name__ == "__main__":
    main()
