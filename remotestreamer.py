from wsgiref.simple_server import make_server
from pyramid.response import Response, FileIter
from pyramid.config import Configurator

def download(request):
    import requests

    url = 'http://www.wswd.net/testdownloadfiles/1GB.zip'
    r = requests.get(url, stream=True)

    response = Response(content_type="application/octet-stream")
    response.app_iter = FileIter(r.raw)
    response.content_disposition = 'attachment; filename="1GB.zip"'
    response.content_length = r.headers['content-length']

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
