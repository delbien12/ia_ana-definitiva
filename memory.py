from datetime import datetime

users = {}
history = {}
warnings = {}

def ensure_user(user):
    if user not in users:
        users[user] = {
            "created": str(datetime.now()),
            "messages": 0
        }
        history[user] = []
        warnings[user] = 0

def save(user, msg, res):
    history[user].append({
        "msg": msg,
        "res": res,
        "time": str(datetime.now())
    })
    users[user]["messages"] += 1