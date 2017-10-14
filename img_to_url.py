from imgurpython import ImgurClient
import configparser
import glob

config = configparser.ConfigParser()
config.read('auth.ini')

client_id = config.get('credentials', 'client_id')
client_secret = config.get('credentials', 'client_secret')

client = ImgurClient(client_id, client_secret)

imgs = '/imgs'

for items in glob.glob('imgs/*'):
    a = client.upload_from_path(items, config=None, anon=True)
    print(a['link'])