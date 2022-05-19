import urllib.request
import re
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv('.env')

YT_API_KEY = os.getenv('YT_API_KEY')


async def yt_query(*terms, api_key=YT_API_KEY):
    ''' GET VIDEO BY BEST MATCH OF QUERY '''

    html = urllib.request.urlopen(
        "https://www.youtube.com/results?search_query=" + '+'.join(term for term in terms))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    url = "https://www.youtube.com/watch?v=" + video_ids[0]
    title = title_from_id(video_ids[0])
    return url
# {
#         'title': title,
#         'url': url
#     }


def url_to_stream(json_data, counter=None):

    try:

        # removes link args
        if url.split('&amp;')[0]:
            url = url.split('&amp;')[0]

        # test this to see if better success rate
        url = json_data['url'].replace(r'youtu.be', r'youtube.com/v/')
        url = url.replace(r'watch?v=', 'v/')

        stream_url = get_bestquality(url).url
        json_data['url'] = stream_url
        return json_data

    # may not work; GOAL: if can't get stream: remove from library
    except ValueError:
        # json_data = json_data.drop(labels=counter, axis=0)
        # json_data = json_data.reset_index(drop=True)
        return json_data


def title_from_id(title, id, api_key=YT_API_KEY):
    print('GETTING TITLE FROM ID')
    url = requests.get(
        f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={id}&key={api_key}')  # .json()
    # url_json = json.loads(url)
    try:
        new_title = url.json()['items'][0]['snippet']['title']
        return new_title
    except:
        return title


# HAVE TO USE API TO GET TITLE
def get_vid_name(json_data, api_key=YT_API_KEY):
    print('GETTING VID NAME')
    print('BEFORE GET NAME:\n', json_data)
    # print(json_data['url'])
    # pattern = r"\??v?=?([^#\&\?]*).*/"
    pattern = '(?:youtube(?:-nocookie)?\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'

    if re.search(pattern, json_data['url']):

        print('IS YOUTUBE LINK')
        id = re.search(pattern, json_data['url']).group(1)
        json_data['title'] = title_from_id(json_data['title'], id)

    print('AFTER GET NAME:\n', json_data)

    return json_data


# def botmain(json_data):

    #
if __name__ == '__main__':
    json_data = {'0': {'title': 'asdfjldshkf',
                       'url': 'https://youtu.be/Hldov3JOopU'}}
    get_vid_name(json_data)


# def try_title(id):
#     youtube = etree.HTML(urllib.request.urlopen(
#         f"http://www.youtube.com/watch?v={id}").read())
#     print(youtube)
#     video_title = youtube.xpath("//span[@id='eow-title']/@title")
#     print(video_title)


# def try_title(VideoID):

    # params = {"format": "json",
    #           "url": "https://www.youtube.com/watch?v=%s" % VideoID}
    # url = "https://www.youtube.com/oembed"
    # query_string = urllib.parse.urlencode(params)
    # url = url + "?" + query_string

    # with urllib.request.urlopen(url) as response:
    #     response_text = response.read()
    #     data = json.loads(response_text.decode())
    #     print(data['title'])
