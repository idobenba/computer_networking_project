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
