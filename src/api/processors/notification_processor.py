import threading

NOTIFICATION_UPDATE_INTERVAL_SEC = 30

# Note: this is just for testing some basic logic!!!

# TODO: expand to:
# - Send push notifications to subscribed mobile devices (e.g. hand-helds)
# - Email export jobs to subscribers
_queue = ["Dummy message"]

def push(notification):
    global _queue
    _queue.append(notification)

def send():
    if len(_queue) > 0:
        notification = _queue.pop(0)
        print(notification)
    threading.Timer(NOTIFICATION_UPDATE_INTERVAL_SEC, send).start()

def start():
    send()