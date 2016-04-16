from twisted.web import server, resource
from twisted.internet import reactor

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
        return "Hello from poker."

root = Root()
poker = PokerInterface()
pcommand = PokerInterface()
root.putChild('poker', poker)
poker.putChild('command', PokerInterface())

site = server.Site(root)
reactor.listenTCP(8080, site)
reactor.run()
