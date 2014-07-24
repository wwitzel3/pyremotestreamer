from collections import defaultdict
from wsgiref.simple_server import make_server
from pyramid.response import Response, FileIter
from pyramid.config import Configurator

download_table = defaultdict(int)

class MeteredFileIter(FileIter):
    def __init__(self, user, file):
        self.user = user
        super(MeteredFileIter, self).__init__(file)

    def next(self):
        val = self.file.read(self.block_size)
        if not val:
            raise StopIteration
        download_table[self.user] += self.block_size
        if download_table[self.user] % (self.block_size * 2) == 0:
            print "User has downloaded: %d" % (download_table[self.user])
        return val
    __next__ = next

def download(request):
    import requests

    url = 'http://www.wswd.net/testdownloadfiles/1GB.zip'
    r = requests.get(url, stream=True)

    response = Response(content_type="application/octet-stream")
    response.app_iter = MeteredFileIter('user1', r.raw)
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
