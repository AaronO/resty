# Resty imports
from resty import RestyServer



# An example handler
class ExampleHandler(object):
    HEADERS = {'Content-Type' : 'text/html'}

    def save(self):
        return "Isn't it a nice day ?"

    def get(self, **kwargs):
        msgs = []
        for k,v in kwargs.items():
            msgs.append("<p><b>%s</b> : %s</p>" % (k,v))
        return ''.join(msgs)

    def delete(self):
        return "It's not very nice :("


# Server
class ExampleServer(RestyServer):
    PORT = 8088
    LISTEN = '0.0.0.0'
    HANDLERS = {'example' : ExampleHandler}



def main():
    ExampleServer().start()


if __name__ == '__main__' :
    main()
