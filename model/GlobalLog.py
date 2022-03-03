log = []
log_subscription = []

def subscribe_to_log(cb):
    if(cb not in log_subscription):
        log_subscription.append(cb)
        
def unsubscribe_to_log(cb):
    if(cb in log_subscription):
        log_subscription.remove(cb)
        
def update_log(msg):
    for sub in log_subscription:
        sub(msg)
        
def add_to_log(msg):
    update_log(msg)
    log.append(msg)
    
    
def clear_log():
    log.clear()