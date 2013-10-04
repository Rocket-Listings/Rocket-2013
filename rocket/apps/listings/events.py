from django_socketio import events, clients




@events.on_connect
def connected(request, socket, context):
    print "connected"
    print socket.session.session_id
    print clients.CLIENTS.keys()

@events.on_disconnect
def disconnected(request, socket, context):
    print "disconnected"
    print socket.session.session_id
