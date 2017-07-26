from __future__ import unicode_literals
import logging
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import Request, Response
from subprocess import check_output, PIPE
import gunicorn
from tempfile import NamedTemporaryFile, mkdtemp
import os

class WebServer(gunicorn.app.base.BaseApplication):

    def __init__(self, application, **options):
        self.options = {
            'worker_class': 'gevent',
        }
        self.application = application
        super(WebServer, self).__init__()

    def load(self):
        return self.application

class WebApp(object):

    def __init__(self, **kw):
        self.log = logging.getLogger(__name__)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            method = getattr(self, 'endpoint_{}'.format(endpoint))
            return method(adapter, request, **values)
        except HTTPException, e:
            return e

    url_map = Map([])


class SomeApp(WebApp):
    def __init__(self):
        WebApp.__init__(self)

    def endpoint_some_endpoint(self, adapter, request):
        contract = NamedTemporaryFile()
        size = 0
        for line in request.input_stream:
            contract.write(line)
            size += len(line)
            if size > 50000:
                return Response('too long', response='400')
        contract.seek(0)
        tmpdir = mkdtemp()
        results = check_output(['solc', contract.name, '--bin', '--abi', '--optimize', '-o', tmpdir])
        return Response('Created the following files:\n\t{}\n'.format(os.listdir(tmpdir)))

    url_map = Map([
        Rule('/some_endpoint', endpoint='some_endpoint', methods=['POST'])
    ])


application = SomeApp()