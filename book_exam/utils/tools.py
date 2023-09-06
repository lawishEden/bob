from threading import Thread
from time import sleep

def asyncc(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

def append_to_hdfs(client, hdfs_path,data):
    client.write(hdfs_path, data, overwrite=False, append=True)

from book_exam import settings
import os

@asyncc
def writeToLocal(filename, data):

    with open(os.path.join(settings.HITS_PATH, filename), 'a') as fp:
        fp.write(data+'\n')

# if __name__ == '__main__':
    # from hdfs import Client
    # hdfs_path = '/book/hit.txt'
    # client = Client('http://node1:9870')
    # append_to_hdfs(client, hdfs_path, 'wewerwer' + '\n')