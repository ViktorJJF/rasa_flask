from rasa.core.channels.channel import UserMessage
from rasa.core.events import SlotSet
dst = agent.tracker_store.get_or_create_tracker(UserMessage.DEFAULT_SENDER_ID)
ss = SlotSet('username', 'Alex')
dst.update(ss)
agent.tracker_store.save(dst)