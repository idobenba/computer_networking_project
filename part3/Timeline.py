import Event
class Timeline:
    def __init__(self):
        self.timeline = []

    def create_timeline(self, host_list_for_events, id, destination_host_list):
        # creates a timeline by creating events for each host in the host list
        # and then appending the events to the timeline, then sorting the timeline
        for host in host_list_for_events:
            host.create_events(id, destination_host_list)
            id += len(host.events)

        for host in host_list_for_events:
            for event in host.events:
                self.timeline.append(event)
        self.timeline.sort(key=lambda x: (x.schedule_time, x.message_id))

    def add_event(self,event):
        self.timeline.append(event)

    def copy_timeline(self, timeline):

        for event in timeline:
            self.timeline.append(event)

    def new_timeline(self):
        self.timeline=[]
        self.timeline.append(Event.Event(1,'create',1,3,11, 1000))
        self.timeline.append(Event.Event( 0, 'create', 0, 3, 9,  1000))
        self.timeline.append(Event.Event( 2,  'create',2, 3, 13,  1000))
        self.timeline.append(Event.Event(1, 'create', 1, 3, 11, 1000))
        self.timeline.append(Event.Event(0, 'create', 0, 3, 9, 1000))
        self.timeline.append(Event.Event(2, 'create', 2, 3, 13, 1000))

        self.timeline.append(Event.Event(3, 'create', 2, 3, 14, 200))
        self.timeline.append(Event.Event(4, 'create', 1, 3, 12, 500))
        self.timeline.append(Event.Event(5, 'create', 0, 3, 10, 1400))

        self.timeline.append(Event.Event( 3, 'create', 2, 3, 14,  200))
        self.timeline.append(Event.Event( 4,  'create',1, 3, 12,  500))
        self.timeline.append(Event.Event( 5, 'create', 0, 3, 10,  1400))
        self.timeline.sort(key=lambda x: (x.schedule_time, x.message_id))
