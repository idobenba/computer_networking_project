class Event:
    def __init__(self, schedule_time, event_type, scheduling_object_id, target_object_id, message_id,message_size=0, priority=None):
        self.schedule_time = schedule_time
        self.event_type = event_type
        self.scheduling_object_id = scheduling_object_id
        self.target_object_id = target_object_id
        self.message_id = message_id
        self.message_size = message_size
        self.priority = priority
