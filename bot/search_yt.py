import urllib.request
import re
import os
import requests
from dotenv import load_dotenv
load_dotenv('.env')

YT_API_KEY = os.getenv('YT_API_KEY')


async def yt_query(api_key, *terms):
    ''' GET VIDEO BY BEST MATCH OF QUERY '''

    html = urllib.request.urlopen(
        "https://www.youtube.com/results?search_query=" + '+'.join(term for term in terms))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    url = "https://www.youtube.com/watch?v=" + video_ids[0]
    title = name_from_id(api_key, video_ids[0])
    return url
# {
#         'title': title,
#         'url': url
#     }


def name_from_id(api_key, id):
    url = requests.get(
        f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={id}&key={api_key}').json()
    # url_json = json.loads(url)
    title = url['items'][0]['snippet']['title']
    return title
    # title = url_json['entry']['title']['$t']
    # return title
    # author = json['entry']['author'][0]['name']


# HAVE TO USE API TO GET TITLE
def get_vid_name(api_key, json_data):
    print(json_data)
    for item in json_data:

        print(json_data[item]['url'])
        # pattern = r"\??v?=?([^#\&\?]*).*/"
        pattern = '(?:youtube(?:-nocookie)?\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'

        if re.search(pattern, json_data[item]['url']):

            print(1)
            id = re.search(pattern, json_data[item]['url']).group(1)
            json_data[item]['title'] = name_from_id(api_key, id)

    print(json_data)
    return json_data


# def botmain(json_data):

    #
if __name__ == '__main__':
    print(YT_API_KEY)
    json_data = {'0': {'title': 'asdfjldshkf',
                       'url': 'https://youtu.be/Hldov3JOopU'}}
    get_vid_name(YT_API_KEY, json_data)


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
