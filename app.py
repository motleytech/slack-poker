from twisted.web import server, resource
from twisted.internet import reactor
import reloader

class Root(resource.Resource):
    isLeaf = False
    def getChild(self, name, request):
        if name == '':
            return self
        return resource.Resource.getChild(self, name, request)

    def render_GET(self, request):
        return "Nothing to see here."

class PokerInterface(resource.Resource):
    isLeaf = True
    def getChild(self, name, request):
        if name == '':
            return self
        return resource.Resource.getChild(self, name, request)

    def render_GET(self, request):
        print request, request.uri
        if request.uri.endswith('command'):
            return "Hello from poker command"
        return "Hello from poker."


def myMain():
    root = Root()
    poker = PokerInterface()
    pcommand = PokerInterface()

    root.putChild('poker', poker)
    poker.putChild('command', pcommand)

    site = server.Site(root)
    port = 8080
    print 'attaching to port %s...' % port
    reactor.listenTCP(port, site)
    reactor.run()


reloader.main(myMain)
#reactor.run()
