# Python imports
import re
import urlparse

# Gevent imports
import gevent
import gevent.http


##
# Simple class for parsing incoming requests
##
class HttpRequest(object):
    def __init__(self, raw_request):
        self.raw_request = raw_request
        self.parse()

    def parse(self):
        self.parse_other()
        self.parse_headers()
        self.parse_url()


    def parse_other(self):
        self.body = self.raw_request.input_buffer
        self.method = self.raw_request.typestr

    def parse_headers(self):
        self.META = dict(self.raw_request.get_input_headers())

        # Add some
        self.META['REMOTE_ADDR'] = self.raw_request.remote


    def parse_url(self):
        info = urlparse.urlparse(self.raw_request.uri)

        # GET
        kvdict = urlparse.parse_qs(info.query)
        self.GET = {}
        for k,v in kvdict.items():
            self.GET[k] = v[0] if len(v) == 1 else v

        # path
        self.path = info.path



##
# Simple Server using gevent's HTTP server
##
class BaseRestyServer(object):
    # Pattern to match
    URL_PATTERN = r"^/(?P<class>\w+)/(?P<method>\w+)"
    # Which IP to listen for
    LISTEN = '127.0.0.1'
    PORT = 12345
    # List of classes to handle responses
    HANDLERS = {}


    def __init__(self, listen = None, port = None, url_pattern = None, handlers = None):
        self.listen = listen or self.LISTEN
        self.port = port or self.PORT
        self.url_pattern = url_pattern or self.URL_PATTERN
        self.handlers = handlers or self.HANDLERS

        # Http server
        self.http_server = gevent.http.HTTPServer((self.listen, self.port), self.dispatch)


    def build_handlers(self):
        for key,klass_obj in self.handlers.items():
            self.handlers[key] = klass_obj()


    def start(self):
        # Setup
        self.build_handlers()
        self.url_regex = re.compile(self.url_pattern)

        # Run
        self.http_server.serve_forever()


    def handle_404(self, request):
        request.add_output_header('Content-Type', 'text/html')
        request.send_reply(404, "Not Found", "<h1>Not Found for : <b>%s</b></h1>" % request.uri)


    def handle_500(self, request, error = None):
        request.add_output_header('Content-Type', 'text/html')
        request.send_reply(500, "Not Found", "<h1>Unexpected Error : <b>%s</b></h1>" % error)


    def handle(self, request, class_name, method_name):
        klass_obj = self.handlers.get(class_name, None)

        if not klass_obj:
            return False

        method = getattr(klass_obj, method_name, None)
        if not method:
            return False

        # Setup headers
        headers = getattr(klass_obj, 'HEADERS', {})
        for key,value in headers.items():
            request.add_output_header(key, value)

        # Call method
        http_request = HttpRequest(request)
        kwargs = http_request.GET
        response = method(**kwargs)

        # Write response
        request.send_reply(200, "OK", response)
        return True


    def dispatch(self, request):
        match = self.url_regex.match(request.uri)
        matchdict = match.groupdict() if match else {}
        class_name = matchdict.get('class', None)
        method_name = matchdict.get('method', None)

        # Nothing to be found
        if not(class_name or method_name):
            self.handle_404(request)
            return

        matched = False
        try:
            matched = self.handle(request, class_name, method_name)
        except Exception as e:
            return self.handle_500(request, e)

        # No match made
        if not matched:
            return self.handle_404(request)



# Sugar syntax
RestyServer = BaseRestyServer
RestyRequest = BaseRestyServer