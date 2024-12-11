import os

# reCaptcha constants
TWOCAP_KEY = os.getenv("TWOCAP_KEY")
RECAP_KEY = "6LfCVLAUAAAAALFwwRnnCJ12DalriUGbj8FW_J39"
RECAP_ON_URL = "https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com%2F"
RECAP_ACTION = "accounts/login"

# Spotify constants and account info
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
CLIENT_VERSION = "1.2.53.257.g47fa6c39"
PLAYLIST_QUERY_HASH = "19ff1327c29e99c208c86d7a9d8f1929cfdf3d3202a0ff4253c821f1901aa94d"
SPOTIFY_ACCOUNT = ("email@gmail.com","password123")

# Training/test data
# First playlist for each genre is Spotify's top 50
# Other playlists include other songs not represented in the 50 best songs (from the genre's page)
TRAINING_DATA_PLAYLISTS = {
    "Hip-Hop":["spotify:playlist:37i9dQZF1DWZFV9Asvj1J9","spotify:playlist:37i9dQZF1DX0XUsuxWHRQd", "spotify:playlist:37i9dQZF1DX2RxBh64BHjQ"],
    "Indie":["spotify:playlist:37i9dQZF1DXdbXrPNafg9d", "spotify:playlist:37i9dQZF1DX4OzrY981I1W", "spotify:playlist:37i9dQZF1DX3ESMLExvnY4"],
    "Pop":["spotify:playlist:37i9dQZF1DX5dpn9ROb26T","spotify:playlist:37i9dQZF1DWUa8ZRTfalHk", "spotify:playlist:37i9dQZF1DWWvvyNmW9V9a", "spotify:playlist:37i9dQZF1DXaPCIWxzZwR1", "spotify:playlist:37i9dQZF1DXca8AyWK6Y7g"],
    "R&B":["spotify:playlist:37i9dQZF1DXcSC8oOed07w", "spotify:playlist:37i9dQZF1DWUzFXarNiofw", "spotify:playlist:37i9dQZF1DX4SBhb3fqCJd"],
    "Dance/Electronic":["spotify:playlist:37i9dQZF1DWUn2FwhH1fMF", "spotify:playlist:37i9dQZF1DX4dyzvuaRJ0n", "spotify:playlist:37i9dQZF1DX8tZsk68tuDw"],
    "Rock":["spotify:playlist:37i9dQZF1DX8YNmLOBjUmx", "spotify:playlist:37i9dQZF1DXcF6B6QPhFDv", "spotify:playlist:37i9dQZF1DWZryfp6NSvtz"],
    "Latin":["spotify:playlist:37i9dQZF1DX8L1VmOcEBjS", "spotify:playlist:37i9dQZF1DWWWpEY2WZLnS", "spotify:playlist:37i9dQZF1DX2shzuwwKw0y"],
    "Country":["spotify:playlist:37i9dQZF1DWXuiFJj5T7Ii", "spotify:playlist:37i9dQZF1DWYUfsq4hxHWP", "spotify:playlist:37i9dQZF1DX8S0uQvJ4gaa"],
    "Folk/Americana":["spotify:playlist:37i9dQZF1DXawR86Jfwxln", "spotify:playlist:37i9dQZF1DXaUDcU6KDCj4", "spotify:playlist:37i9dQZF1DWTyjRnMgESue"],
    "Jazz":["spotify:playlist:37i9dQZF1DX5LYxFep0J7E", "spotify:playlist:37i9dQZF1DXcWL5K0oNHcG", "spotify:playlist:37i9dQZF1DX7YCknf2jT6s"],
    "Christian/Gospel":["spotify:playlist:37i9dQZF1DXbrknLz4Do7C", "spotify:playlist:37i9dQZF1DWVYgpMbMPJMz", "spotify:playlist:37i9dQZF1DWUileP28ODwg"],
    "K-Pop":["spotify:playlist:37i9dQZF1DWYlzvIAycznp", "spotify:playlist:37i9dQZF1DX4FcAKI5Nhzq", "spotify:playlist:37i9dQZF1DX14fiWYoe7Oh"],
    "Musica Mexicana":["spotify:playlist:37i9dQZF1DX1k7CwwZgd48", "spotify:playlist:37i9dQZF1DX905zIRtblN3", "spotify:playlist:37i9dQZF1DX6Adf5JEwIPs"],
    "Reggaeton":["spotify:playlist:37i9dQZF1DWZI5fbMaBtko", "spotify:playlist:37i9dQZF1DXbSbnqxMTGx9", "spotify:playlist:37i9dQZF1DWYtKpmml7moA"],
    "Metal":["spotify:playlist:37i9dQZF1DX5FZ0gGkvIRf", "spotify:playlist:37i9dQZF1DX5J7FIl4q56G", "spotify:playlist:37i9dQZF1DX9qNs32fujYe"],
    "Blues":["spotify:playlist:37i9dQZF1DWYi488IywmOA","spotify:playlist:37i9dQZF1DXd9rSDyQguIk", "spotify:playlist:37i9dQZF1DXcu3QLJudo4X"],
    "Funk":["spotify:playlist:37i9dQZF1DX9FWIO38pHuz", "spotify:playlist:37i9dQZF1DX70TzPK5buVf", "spotify:playlist:37i9dQZF1DWZgauS5j6pMv"],
    "Kids":["spotify:playlist:37i9dQZF1DXbfRwViuerGJ", "spotify:playlist:37i9dQZF1DX6r25lY14UGk", "spotify:playlist:37i9dQZF1DXd4bJEFQJTXh"]
}

TEST_DATA_PLAYLISTS = {
    "Hits":"spotify:playlist:37i9dQZF1DWVmX5LMTOKPw",
    "Viral":"spotify:playlist:37i9dQZF1DX7EqpAEG8F4f",
    "Fresh Finds":"spotify:playlist:37i9dQZF1DX7EqpAEG8F4f",
    "EQUAL US 2024":"spotify:playlist:37i9dQZF1DWU86q8CK6tXo",
    "TV & Movie Tracks": "spotify:playlist:37i9dQZF1DWVYasTznT0KT",
    "Ultimate End of Year Mixtape": "spotify:playlist:37i9dQZF1DX8sljIJzI0oo",
    "Frequency 2024": "spotify:playlist:37i9dQZF1DWVgsJtp58d1t",
    "RADAR US 2024": "spotify:playlist:37i9dQZF1DWY0DyDKedRYY",
    "Indie Gems":"spotify:playlist:37i9dQZF1DWZw4RckG6Eyg",
    "Rock Gems":"spotify:playlist:37i9dQZF1DX2H2Plf6Ogpv"
}

# Miscellaneous
LOGGING_FILE = "log.txt"
CLEAR_DATABASE_ON_RESTART = False