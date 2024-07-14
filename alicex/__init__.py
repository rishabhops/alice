from alicex.core.bot import alice
from alicex.core.dir import dirr
from alicex.core.git import git
from alicex.core.userbot import Userbot
from alicex.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = alice()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
