"""Sort message exports into reply, review, and waiting queues."""
from runtime import *

from datetime import timedelta
def process(data):
    now = instant(data["now"])
    hours = number(data["sla_hours"], "sla_hours", 0.01)
    vip = {x.casefold() for x in strings(data["vip_senders"], "vip_senders")}
    messages = records(data, "messages")
    unique(messages)
    queues = {k:[] for k in ("reply_now","reply_later","review","waiting","closed")}
    for item in messages:
        received = instant(item["received_at"])
        if received > now:
            raise ValueError("received_at cannot be in the future")
        sender = text(item.get("sender"), "sender")
        status = choice(item.get("status"), ("open","waiting","closed"), "status")
        if type(item.get("needs_reply")) is not bool:
            raise ValueError("needs_reply must be boolean")
        due = received + timedelta(hours=hours)
        urgent = now >= due
        is_vip = sender.casefold() in vip
        if status != "open":
            queue, reason = status, status
        elif not item["needs_reply"]:
            queue, reason = "review", "no_reply_requested"
        elif urgent or is_vip:
            queue, reason = "reply_now", "overdue" if urgent else "vip"
        else:
            queue, reason = "reply_later", "within_sla"
        queues[queue].append(dict(item, age_hours=round((now-received).total_seconds()/3600,2), due_at=due.isoformat(), reason=reason))
    for queue in queues.values():
        queue.sort(key=lambda x:(0 if x["reason"]=="overdue" else 1,x["due_at"],x["id"]))
    return {"as_of":now.isoformat(),"queues":queues}

if __name__ == "__main__":
    sys.exit(main(process, "Sort message exports into reply, review, and waiting queues."))
