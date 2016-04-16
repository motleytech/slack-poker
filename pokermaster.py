
# the master poker application
# can run one poker session per (team, channel) combination.

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

commandName = "/poker"
validPoints = [1, 2, 3, 5, 8, 13, 21, 34]


class Session(object):
    def __init__(self, team, channel, storyid):
        self.sessionid = (team, channel)
        self.storyid = storyid
        self.team = team
        self.channel = channel
        self.users = []
        self.votes = []


class PokerMaster(object):
    def __init__(self):
        self.sessions = {}
        self.cache = {}

    def processCommand(self, command, details):
        if len(command) == 0:
            self.sendHelpInfo(details)

        cmd = command[0]
        if cmd == 'start':
            self.processStartCommand(command, details)
        elif cmd == 'end':
            self.processEndCommand(command, details)
        elif cmd == 'vote':
            self.processVote(command, details)
        elif cmd == 'help':
            self.sendHelpInfo(details)

        self.sendError('Unrecognized command {cmd}. Try "{cmdName} help" for possible commands.'.format(cmd=cmd, cmdName=commandName))

    def processStartCommand(self, command, details):
        if len(command) != 2:
            return self.sendError('Incorrect number of arguments for "start" command. Correct usage: "{cmdName} start story_id"'.format(cmdName=commandName))
        if command[1] == "":
            return self.sendError('Incorrect id for story_id. Use any valid string or number for story id: "{cmdName} start story_id"'.format(cmdName=commandName))

        if self.sessionExists(details):
            return self.sendError('Cannot start another session until previous one still open. Use "{cmdName} status" to know more about the open session or "{cmdName} end" to end the last session'.format(cmdName=commandName))

        return self.startSession(command, details)

    def processEndCommand(self, command, details):
        if len(command) != 1:
            return self.sendError('Incorrect number of arguments for the "end" command. Correct usage: "{cmdName} end"'.format(cmdName=commandName))
        return self.endSession(details)

    def processVoteCommand(self, command, details):
        if len(command) != 2:
            return self.sendError('Incorrect number of arguments for the "vote" command. Correct usage: "{cmdName} vote points"'.format(cmdName=commandName))
        try:
            points = int(command[1])
            if points not in validPoints:
                return self.sendError('Error: Bad choice of points. Valid point choices are {pointChoices}'.format(pointChoices=validPoints))
        except:
            return self.sendError('Error: Points needs to be one of {pointChoices}'.format(pointChoices=validPoints))

        self.countVote(command, details)

    def countVote(self, command, details):
        points = int(command[1])
        session = self.getSession(details)
        userid = self.getUser(details)
        session.votes[userid] = points

        if self.allVoted():
            reactor.callLater(self.endSession, details)

        return self.ackVote()

    def endSession(self, details):
        sessionid = self.getSessionId(details)
        session = self.sessions[sessionid]
        del self.sessions[sessionid]
        self.oldSessions[sessionid] = session

        return self.formFinalResult(session)

    def formFinalResult(self, session):
        finalPoints = self.calculatePoints(session)
        status = self.getVoteStatus(session)

        return "final result: 5.55 points"

    def createSession(self, storyid, details):
        team = self.getTeam(details)
        channel = self.getChannel(details)
        session = Session(team, channel, storyid)
        self.sessions[session.sessionid] = session

    def isUserDataCached(self, session):
        return False

    @inlineCallbacks
    def getUserInfo(self, session):
        pass


    def startSession(self, command, details):
        storyid = command[1]
        session = self.createSession(storyid, details)

        if not self.isUserDataCached(session):
            self.getUserInfo(session)
            return self.sendMessage('Creating planning poker session... getting user information.')
        else:
            pass



        team = self.getTeam(details)
        channel = self.getChannel(details)
        teamUserData = self.cache.get('%s/users' % details.team)
        channelUserData = self.cache.get('%s/%s/users' % details.team)
