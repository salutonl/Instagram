#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from pyquery import PyQuery as pq
import json
import re
import os
import sys
import time
import random
from hashlib import md5


# In[2]:


basic_url = 'https://www.instagram.com/celinefarach/'
source_page = 'https://www.instagram.com/graphql/query/?query_hash=a5164aed103f24b03e7b7747a2d94e3c&variables=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A12%2C%22after%22%3A%22{cursor}%22%7D'


# In[3]:


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    'cookie': 'mid=W76rMwALAAGCXSt7H2TpGxVwM0NU; mcd=3; csrftoken=ffSDTujqssh6xNu2kUIDF7CFQbQ4u6tQ; ds_user_id=7176654068; sessionid=7176654068%3ALAyfuf8201U4Gu%3A23; fbm_124024574287414=base_domain=.instagram.com; shbid=5791; rur=FTW; fbsr_124024574287414=U6Zd7MX6cAu6N4dFafFEpY3GDEGI9S9zgIGN7LfB9WU.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUNQVkxiYnQxdjRyeHY1N1BCV21qeXZZdndycWZmMHdOU1ZuNHBvbEZyUTlsUklqOTRqUGJZclhHWmluN1RzNXlfMHBSQjJnLWdkbVZSNEpvenpDME9xNmJ3NmdlUVJqOTRLWVZ1OFd3b3NVS3A3eFBfWlpqLWNxUDVWSjBhTWFweGFQdGlnekh5Q2NTcWFnWm9FY096UEUyYkI3dkJGVmt1RWhkOXljc2FQQ0xJLVdQMU02Wm9tUlJ4SGdjeVJ2SHNaNFN1d0NPbE5UeDVINHFrOXZ2NklaYXU3empyNkhBdDBydmJVbDY3eEhGazNTSWh6RDFGNWp2WlF6anZvZjBvNEk1UUIycmVLMjUxVXd1bEd1bVlsQmQxU3VxdWNTRjVfOUhyTS1DWTI5eThDQU9fYW5Yc3ZsUlNaN3duLXJ3cnh6V2xKS0kyT2FWNGRWcWdVcDB4RSIsImlzc3VlZF9hdCI6MTU0MDg4OTg3NywidXNlcl9pZCI6IjEwMDAyMjkyMzM0MTc1MCJ9; urlgen="{\"103.106.53.173\": 131613\054 \"103.106.53.130\": 131613\054 \"47.75.200.191\": 45102}:1gHPqf:zx7qwQZl4ij1hOiKSAcwChqyUTs"'
}


# In[4]:


def get_source_page(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print('request source page success!')
            return response.text
        else:
            print('request source page failed! the status code is ' + response.status_code)
            return None
    except Exception as e:
        print(e)
        return None


# In[5]:


def get_image_resource(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print('get image success!')
            return response.content
        else:
            print('get image failed' + response.status_code)
            return None
    except Exception as e:
        print(e)
        return None


# In[6]:


def get_other_page(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print('request json error, status code :', response.status_code)
    except Exception as e:
        print(e)
        return get_other_page(url)


# In[7]:


def get_images_urls(first_page_source):
    urls = []
    user_id = re.findall('"profilePage_([0-9]+)"', first_page_source, re.S)[0]
    doc = pq(first_page_source)
    items = doc('script[type="text/javascript"]').items()
    for item in items:
        if item.text().strip().startswith('window._sharedData'):
            js_data = json.loads(item.text()[21:-1], encoding='utf-8')
            edges = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
            page_info = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]['page_info']
            cursor = page_info['end_cursor']
            page_exit = page_info['has_next_page']
            for edge in edges:
                if edge['node']['display_url']:
                    display_url = edge['node']['display_url']
                    print(display_url)
                    urls.append(display_url)
    while page_exit:
        url = source_page.format(user_id=user_id, cursor=cursor)
        js_data = get_other_page(url)
        infos = js_data['data']['user']['edge_owner_to_timeline_media']['edges']
        cursor = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        page_exit = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        for info in infos:
            if info['node']['is_video']:
                video_url = info['node']['video_url']
                if video_url:
                    urls.append(video_url)
            else:
                if info['node']['display_url']:
                    display_url = info['node']['display_url']
                    urls.append(display_url)
    return urls


# In[8]:


def main():
    page_source = get_source_page(basic_url)
    urls = get_images_urls(page_source)
    dirpath = r'D:\Instagram\celinefarach'
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    for i in range(len(urls)):
        try:
            image_soure = get_image_resource(urls[i])
            file_path = r'D:\Instagram\celinefarach\{0}.{1}'.format(md5(image_soure).hexdigest(), urls[i][-3:])
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    print('This is the {0} picture downloading'.format(i))
                    f.write(image_soure)
                    f.close()
            else:
                print('the {0} picture has already exits'.format(i))
        except Exception as e:
            print(e)
    


# In[9]:


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    spend_time = end - start
    hour = spend_time // 3600
    minutes = (spend_time - 3600 * hour) // 60
    second = spend_time - 3600 * hour - 60 * minutes
    print(f'totally cost {hour}hours {minutes}minutes and {second}seconds')


# In[ ]:




