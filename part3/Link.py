import queue

import Event


class Link:
    def __init__(self, object_id, host1, host2, transmission_rate=1000, prop_delay=0, error_rate=0):
        self.object_id = object_id
        self.host1 = host1
        self.host2 = host2
        self.transmission_rate = transmission_rate
        self.prop_delay = prop_delay
        self.error_rate = error_rate
        self.time_sent = 0
        self.link_queue = queue.Queue()
        self.timeline = []
        self.trans_size = 0
        self.time_to_receive = 0

    def send_message(self, message, host_list, print_flag=False, start_time=0):
        # Send a message to the destination host in the host list
        dst_host = host_list[message.dst_address]
        dst_host.receive_message(message, self, print_flag, start_time=start_time)

    def send_message_to_switch(self, message, target_switch, host_list, switch_list, link_list, print_flag=False,
                               start_time=0):
        # Send a message to a target switch
        target_switch.receive_message(message, self, host_list, switch_list, link_list, print_flag,
                                      start_time=start_time)

    def send_message_to_switch_part_2(self, message, target_switch, destination_host_list, switch_list, link_list,
                                      print_flag=False,
                                      curr_time=0):
        # Send a message to a target switch
        target_switch.receive_message_part_2(message, self, destination_host_list, switch_list, link_list, print_flag,
                                             curr_time=curr_time)

    def send_message_to_switch_part_3(self, message, target_switch, destination_host_list, switch_list, link_list,
                                      print_flag=False, curr_time=0):

        if self.time_sent <= message.schedule_time:
            self.time_to_receive = message.message_size / self.transmission_rate + self.prop_delay + message.schedule_time
        else:
            self.time_to_receive = message.message_size / self.transmission_rate + self.prop_delay + self.time_sent

        target_switch.receive_message_part_3(message, self, destination_host_list, switch_list, link_list, print_flag,
                                             curr_time=self.time_to_receive)

        self.update_timeline(
            Event.Event(self.time_to_receive, "receive from host", self.host1.address, self.host2.address,
                        message.message_id))

    def send_message_from_switch(self, message, target_host, print_flag=False, curr_time=0):
        # Send a message from a switch to a target host
        target_host.receive_message(message, self, print_flag, curr_time=curr_time)

    def send_message_from_switch_part_2(self, message, target_host, print_flag=False, curr_time=0):
        # Send a message from a switch to a target host
        target_host.receive_message(message, self, print_flag, curr_time=curr_time)

    def send_message_from_switch_part_3(self, message, target_host, print_flag=False, curr_time=0, event=None):
        # Send a message from a switch to a target host
        self.host2.packets_sent += 1
        if self.time_sent <= message.schedule_time:
            self.time_to_receive = (
                                               message.message_size / self.transmission_rate) + self.prop_delay + + message.schedule_time
        else:
            self.time_to_receive = message.message_size / self.transmission_rate + self.prop_delay + self.time_sent
        target_host.receive_message(message, self, print_flag, curr_time=self.time_to_receive,
                                    time_to_receive=self.time_to_receive)
        self.update_timeline(Event.Event(self.time_to_receive, "receive from switch", self.host2.address,
                                         self.host1.address, message.message_id))

    def send_message_from_switch_to_switch(self, message, target_switch, host_list, print_flag=False, start_time=0):
        # Send a message from a switch to another switch
        target_switch.receive_message_from_switch(message, self, host_list, print_flag, start_time=start_time)

    def is_link_busy(self, curr_time, message_size):
        # Check if the link is busy by comparing the current time with the time the last message was sent and the time
        # it takes to send the current message
        if self.time_sent == 0:
            return False
        else:
            if self.time_sent + self.prop_delay + (message_size / self.transmission_rate) < curr_time:
                return False
        return True

    def is_link_busy_part_3(self, curr_time):
        # Check if the link is busy by comparing the current time with the time the last message was sent and the time
        # it takes to send the current message
        curr_time = round(curr_time, 10)
        transmission_time = round(self.time_sent + self.prop_delay + (self.trans_size / self.transmission_rate), 10)
        if self.time_sent == 0:
            return False
        else:
            if transmission_time <= curr_time:
                return False
        return True

    def update_timeline(self, event):
        self.timeline.add_event(event)
        self.timeline.timeline.sort(key=lambda x: (x.schedule_time, x.message_id))

    def get_timeline(self, timeline):
        self.timeline = timeline
