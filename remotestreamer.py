from collections import defaultdict
from wsgiref.simple_server import make_server
from pyramid.response import Response, FileIter
from pyramid.config import Configurator

# this is your persistence layer. some keyvalue store with good read/write performance.
download_table = defaultdict(int)

def update_download_table(user, bytes):
    download_table[user.name] += bytes


class User(object):
    def __init__(self, name, credit):
        self.name = name
        self.credit = credit # in bytes

    def has_enough_credit(self, block_size):
        return self.credit >= block_size

    def add_credit(self, credit):
        self.credit += credit

    def deduct_credit(self, credit):
        update_download_table(self, credit)
        self.credit -= credit

    def display_download_stats(self):
        print "%s has downloaded %d bytes." % (self.name, download_table[self.name])


class MeteredFileIter(FileIter):
    def __init__(self, user, file):
        self.user = user
        super(MeteredFileIter, self).__init__(file)

    def next(self):
        if not self.user.has_enough_credit(self.block_size):
            print "Not enough credit to coninute download"
            raise StopIteration

        val = self.file.read(self.block_size)
        if not val:
            raise StopIteration

        self.user.deduct_credit(self.block_size)
        self.user.display_download_stats()

        return val
    __next__ = next

def download(request):
    import requests
    url = 'http://www.wswd.net/testdownloadfiles/1GB.zip'
    r = requests.get(url, stream=True)

    user = User('user1', 1000000)

    response = Response(content_type="application/octet-stream")
    response.app_iter = MeteredFileIter(user, r.raw)
    response.content_disposition = 'attachment; filename="1GB.zip"'
    response.content_length = int(r.headers['content-length'])

    return response

def main():
    config = Configurator()
    config.add_route('download', '/')
    config.add_view(download, route_name='download')
    app = config.make_wsgi_app()
    return app

if __name__ == '__main__':
    app = main()
    server = make_server('0.0.0.0', 6547, app)
    print ('Starting up server on http://localhost:6547')
    server.serve_forever()
