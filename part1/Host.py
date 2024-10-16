import Message
import Event

import numpy as np
import time


class Host:
    def __init__(self, address, nic, object_id):
        self.address = address
        self.nic = nic
        self.object_id = object_id
        self.total_sent = 0
        self.total_rec = 0
        self.timeline = []
        self.events = []
        self.packets_sent = 0
        self.packets_rec = 0

    def create_message(self, src_address, dest_address, message_size,
                       message_id, schedule_time, start_time, print_flag=False):

        message = Message.Message(message_id, src_address, dest_address,
                                  message_size, start_time)
        message.schedule_time = schedule_time
        self.total_sent += message.message_size
        self.packets_sent += 1
        if print_flag:
            print(f'Host <{self.address}> created an L2 Message (size:<{message.message_size}>)')

        return message

    def receive_message(self, message, link, print_flag=False,start_time=0):
        if message.message_type == "Data":
            if message.dst_address == self.address:
                self.total_rec += message.message_size
                self.packets_rec += 1
                if print_flag:
                    time_destroyed = time.time() - message.start_time
                    print(
                        f'Host <{self.address}> destroyed an L2 Message (size:<{message.message_size}>) at time'
                        f' <{time_destroyed}>')
                del message

    def create_timeline(self, number_of_packets):
        timeline = np.random.exponential(10, size=number_of_packets)
        self.timeline = np.cumsum(timeline)

    def create_events(self, object_id, host_list):
        for time_slot in self.timeline:
            temp_host_list = [host for host in host_list if host.address != self.address]
            dst_host = np.random.choice(temp_host_list)
            event = Event.Event(time_slot, "create", self.address, dst_host.address, object_id)
            self.events.append(event)
            object_id += 1

    def print_total_stats(self, print_flag):
        if print_flag:
            print(f'Host <{self.address}> sent <{self.total_sent}> bytes in <{self.packets_sent}> packets')
            print(f'Host <{self.address}> received <{self.total_rec}> bytes in <{self.packets_rec}> packets')

    def print_average_stats(self, print_flag, number_of_hosts):
        # if print_flag:
        print(f'Host <{self.address}> sent <{self.total_sent / self.packets_sent}> bytes per packet')
        print(f'Host <{self.address}> received <{self.total_rec /  self.packets_sent}> bytes per packet')

    def get_id(self):
        return self.address