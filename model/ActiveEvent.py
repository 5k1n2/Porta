from model import GlobalLog

event_subscription = []

def subscribe_to_activechange(cb):
    if(cb not in event_subscription):
        event_subscription.append(cb)
        
def unsubscribe_to_activechange(cb):
    if(cb in event_subscription):
        event_subscription.remove(cb)
        
def update_active(msg):
    GlobalLog.add_to_log("Server Status changed to {}".format(msg))
    for sub in event_subscription:
        sub(msg)