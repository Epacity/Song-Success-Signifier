# Song Success Signifier

import logging
import sys
import time

from captcha_solver import create_solve_task, get_solve_response
from config import CLEAR_DATABASE_ON_RESTART, LOGGING_FILE, SPOTIFY_ACCOUNT, TRAINING_DATA_PLAYLISTS
from genre_db import clear_database, create_genre_collection
from spotify import Account, SpotifyClient, clean_lyrics
from topic_classifier import generate_topic

def main():
    # Logger setup
    logger = logging.getLogger("Scraper")
    logging.basicConfig(format="[%(asctime)s][%(levelname)s] %(message)s", filename=LOGGING_FILE, encoding="utf-8", level=logging.INFO)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    # Spotify setup
    account = Account(SPOTIFY_ACCOUNT[0], SPOTIFY_ACCOUNT[1])
    logger.info("Initializing...")
    err = account.get_ctx()
    if err:
        logger.fatal(f"Could not make initial connection to Spotify: {err}")
        sys.exit()

    logger.info("Solving reCaptcha before logging in...")
    task_id, err = create_solve_task()
    if err:
        logger.fatal(f"Could not create captcha solve request: {err}")
        sys.exit()

    captcha_response = None
    while captcha_response is None:
        time.sleep(10)
        logger.info("Polling for captcha response...")
        captcha_response, err = get_solve_response(task_id)
        if err:
            logger.fatal(f"Could not solve captcha: {err}")
            sys.exit()

        if not captcha_response:
            logger.info("Captcha not ready yet, waiting 10 seconds before retrying...")

    logger.info("Successfully solved captcha!")
    logger.info(f"Logging into Spotify account ({SPOTIFY_ACCOUNT[0]})...")
    err = account.login(captcha_response)
    if err:
        logger.fatal(f"Could not login to Spotify: {err}")
        sys.exit()

    logger.info("Getting authorization token...")
    err = account.get_bearer_token()
    if err:
        logger.fatal(f"Could not get authorization token: {err}")
        sys.exit()

    logger.info("Getting client token...")
    err = account.get_client_token()
    if err:
        logger.fatal(f"Could not get client token: {err}")
        sys.exit()

    logger.info("Spotify setup complete!")
    client = SpotifyClient(account)

    input("Press enter to begin scraping >>> ")

    all_songs = []
    current_genre = 1
    for genre, playlist_ids in TRAINING_DATA_PLAYLISTS.items():
        to_remove = []
        songs = []
        logger.info(f"Scraping {genre} songs ({current_genre}/{len(TRAINING_DATA_PLAYLISTS)})...")

        curr_playlist = 0
        for playlist_id in playlist_ids:
            playlist_songs, err = client.get_tracks_from_playlist(playlist_id)
            if err:
                logger.error(f"Could not get songs from the {genre} playlist: {err}")
                logger.info("Continuing to the next genre...")
                continue

            for song in playlist_songs:
                # Filter duplicate songs
                if song["id"] in all_songs:
                    logger.info(f"{song['title']} is a duplicate, continuing...")
                    to_remove.append(song)
                    continue

                all_songs.append(song["id"])
                logger.info(f"Getting lyrics for {song['title']}...")
                lyrics, err = client.get_song_lyrics(song["id"], song["image"])
                if err:
                    logger.error(f"Could not get lyrics for {song['title']}: {err}")
                    to_remove.append(song)

                    if err == "Rate limited (408)" or err == "Bad status code: 403":
                        time.sleep(30)

                    continue

                song["lyrics"] = clean_lyrics(lyrics)

                logger.info(f"Generating a topic for {song['title']}...")
                topic, err = generate_topic(song["lyrics"])
                if err:
                    logger.error(f"Could not create a topic for {song['title']}: {err}")
                    to_remove.append(song)
                    continue

                song["topic"] = topic
                song["genre"] = genre
                if curr_playlist == 0:
                    song["in_top_50"] = True

                else:
                    song["in_top_50"] = False

                songs.append(song)

            curr_playlist += 1

        for song in to_remove:
            if song in songs:
                songs.remove(song)

        logger.info(f"Finished analyzing all {genre} songs!")
        logger.info(f"Adding {genre} to database...")

        db_response, err = create_genre_collection(genre, songs)
        if err:
            logger.error(f"Could not add {genre} to database: {err}")

        current_genre += 1

    logger.info("Successfully scraped every genre!")

if __name__ == "__main__":
    if CLEAR_DATABASE_ON_RESTART:
        clear_database()

    main()