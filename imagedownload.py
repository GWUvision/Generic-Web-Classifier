import datetime
import gevent
import hashlib
import os
import csv
import requests
import http.client
import ssl
import time

import urllib.request
import pandas as pd

from gevent import monkey, socket
from gevent.pool import Pool

from socket import timeout
from socket import error as SocketError
from urllib.parse import urlparse

monkey.patch_socket()
pool = Pool(100)
os.makedirs('test/', exist_ok=True)

df = pd.read_csv('output.csv', error_bad_lines=False)

# print(df)
df.columns = ['url', 'extra']
df.drop(['extra'], axis=1, inplace=True)
# print(df.head())
df.index.names = ['index']
df.reset_index(inplace=True)
# print(df.head())
# url_list = df[['index', 'url']].tolist()
url_list = df.values.tolist()
# print(url_list)

# camera_urls = []
# for camera in cameras:
#     # append the index, url, and current hash to a list
#     camera_urls.append([camera[0], camera[2], camera[7]])


# Using threading to download files here
def download_file(index, url):
    # print('starting %s' % url)
    try:
        #context = ssl._create_unverified_context()
        data = urllib.request.urlopen(url, timeout=3).read()
        filepath = '258.{0}.jpg'.format((str(index+1)).zfill(4))

        f = open('test/{0}'.format(filepath), 'wb')
        f.write(data)
        f.close()
        print("[INFO] Image from {0} is different. Saving image...".format(index+1))

    except urllib.error.HTTPError as err:
        print(err)
    except urllib.error.URLError as err:
        print(err)
    except timeout as err:
        print(err)
    except http.client.HTTPException as err:
        print(err)
    except http.client.IncompleteRead as err:
        print(err)
    except http.client.ImproperConnectionState as err:
        print(err)
    except http.client.RemoteDisconnected as err:
        print(err)
    except ConnectionResetError as err:
        print(err)
    except SocketError as err:
        print(err)

begin = time.time()
jobs = [pool.spawn(download_file, index, url) for index, url in url_list]
end = time.time()
print('time: ', end-begin)
print('Downloaded images')
