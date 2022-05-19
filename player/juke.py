import argparse
import sys
import jukebot
import getreddit

parser = argparse.ArgumentParser(
    prog='juke', usage='%(prog)s [options] source', description='Play audio from links')
parser.add_argument(
    '-r', '--reddit', help='Play list of most recent YT submissions from reddit', required=False)
args = vars(parser.parse_args())

if args['reddit']:
    print('Fetching music from entered subreddit')
    try:
        playlist = getreddit.get_yt_subs(args['reddit'])
        print('Playlist obtained! Starting Player...')
        jukebot.main(playlist)
    except:
        print(
            'Something went wrong.\n It is likely that the input is not a valid subreddit.')
