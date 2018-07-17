#!/pless_nfs/home/krood20/AMOSEast/env/bin/python
import datetime
import gevent
import hashlib
import os
import csv
import requests
import http.client
import urllib.request
import pandas as pd

from gevent import monkey, socket
from gevent.pool import Pool

from socket import timeout
from socket import error as SocketError
from urllib.parse import urlparse

monkey.patch_socket()
pool = Pool(30)

df = pd.read_csv('output.csv', error_bad_lines=False)

# print(df)
df.columns = ['url', 'extra']
df.drop(['extra'], axis=1, inplace=True)
print(df.head())

url_list = df['url'].tolist()
print(url_list)

# TODO: Figure out how to get index from dataframe and put in a list in a list with the index and the url and then thread it

# camera_urls = []
# for camera in cameras:
#     # append the index, url, and current hash to a list
#     camera_urls.append([camera[0], camera[2], camera[7]])


# Using threading to download files here
def download_file(index, url):
    # print('starting %s' % url)
    try:
        data = urllib.request.urlopen(url, timeout=5).read()
        filename = os.path.basename('258_{0}'.format(index))
        filepath = '%s/%s_%s.jpg' % (index, index, filename)

        os.makedirs('test/{0}'.format(index), exist_ok=True)
        f = open('test%s/258_%s.jpg' % (index, index, filename), 'wb')
        f.write(data)
        f.close()
        print("[INFO] Image from Camera %s is different. Saving image..." % (index))

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


jobs = [pool.spawn(download_file, url)
        for url in url_list]

print('Downloaded images')
