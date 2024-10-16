import queue


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

    def send_message(self, message, host_list, print_flag=False,start_time =0):
        # Send a message to the destination host in the host list
        dst_host = host_list[message.dst_address]
        dst_host.receive_message(message, self, print_flag,start_time=start_time)

    def send_message_to_switch(self, message, target_switch, host_list, switch_list, link_list, print_flag=False,start_time = 0):
        # Send a message to a target switch
        target_switch.receive_message(message, self, host_list, switch_list, link_list, print_flag,start_time=start_time)

    def send_message_from_switch(self, message, target_host, print_flag=False,start_time= 0):
        # Send a message from a switch to a target host
        target_host.receive_message(message, self, print_flag,start_time = start_time)

    def send_message_from_switch_to_switch(self, message, target_switch, host_list, print_flag=False,start_time=0):
        # Send a message from a switch to another switch
        target_switch.receive_message_from_switch(message, self, host_list, print_flag,start_time = start_time)

    def is_link_busy(self, curr_time, message_size):
        # Check if the link is busy by comparing the current time with the time the last message was sent and the time
        # it takes to send the current message
        if self.time_sent == 0:
            return False
        else:
            if self.time_sent + self.prop_delay + (message_size / self.transmission_rate) < curr_time:
                return False
        return True


