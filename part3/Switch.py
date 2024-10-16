import Host
import Message
import time
import Scheduling
from collections import deque


class Switch:
    def __init__(self, address, number_of_io_ports, queue_type, isFluid=False, scheduling_algorithm="FIFO"):
        self.address = address
        self.number_of_io_ports = number_of_io_ports
        self.output_ports = []
        self.io_ports = [None] * number_of_io_ports  # list of links
        self.mac_table = [None] * 3  # list of MAC addresses
        self.used_ports = 0
        self.isFluid = isFluid
        self.queue_type = queue_type
        self.scheduling_algorithm = scheduling_algorithm
        self.total_hol_time = 0
        self.switch_queues = []
        self.hol_blockers = []
        self.last_departure_time = 0
        self.first_departure_time = 0
        self.packets_rec = 0
        self.packets_sent = 0

    def initialize_port(self, port, link):
        if port < 0 or port > self.number_of_io_ports:
            print("Invalid port number")
        else:
            self.io_ports[port] = link
            self.used_ports += 1

    def create_queues(self, number_of_queues, number_of_input_ports=0):
        if self.queue_type == "input" or self.queue_type == "output":
            self.switch_queues = [deque() for _ in range(number_of_queues)]
            self.hol_blockers = [[0, 0] for _ in range(number_of_queues)]
        elif self.queue_type == "output":
            self.switch_queues = [deque() for _ in range(number_of_queues)]
            self.hol_blockers = [[0, 0] for _ in range(number_of_queues)]
        else:  # virtual
            number_of_output_ports = number_of_queues - number_of_input_ports
            self.switch_queues = [[deque() for _ in range(number_of_output_ports)] for _ in
                                  range(number_of_input_ports)]
            self.hol_blockers = [[[0, 0] for _ in range(number_of_output_ports)] for _ in range(number_of_input_ports)]

    def add_to_table(self, mac_address, port, message, link_list, print_flag=False, curr_time=0):
        found_entry = None
        for entry in self.mac_table:
            if entry is None:
                continue
            elif entry[1] == mac_address:
                found_entry = self.mac_table.index(entry)
                break
        if found_entry is not None:  # mac address already exists in table
            self.mac_table[found_entry][0] = 'True'
            self.mac_table[found_entry][2] = port
            self.mac_table[found_entry][3] = curr_time  # updates TTL
        else:  # mac address does not exist in table
            if None in self.mac_table:  # there is an empty entry
                self.mac_table[self.mac_table.index(None)] = [True, mac_address, port, curr_time]

            else:  # replace the oldest entry
                oldest_entry = self.get_oldest_entry()
                self.mac_table[self.mac_table.index(oldest_entry)] = [True, mac_address, port,
                                                                      curr_time]
            if print_flag:
                self.print_mac_table(link_list)
            return "flood"
        return "added"

    def check_TTL(self, entry):
        if abs(time.time() - entry[3]) >= entry[3]:
            return True
        else:
            return False

    def get_oldest_entry(self):
        oldest_entry = self.mac_table[0][3]
        for entry in self.mac_table:
            if entry[3] < oldest_entry:
                oldest_entry = entry[3]
        for entry in self.mac_table:
            if entry[3] == oldest_entry:
                return entry

    def flooding(self, host_list, message, switch_list=[], start_time=0):
        valid_links = [links for links in self.io_ports if links.host1 != message.src_address]
        for link in valid_links:
            if type(link.host1) == Host.Host:  # switch to host
                link.send_message_from_switch(message, link.host1, start_time=start_time)
            else:  # switch to switch
                if link.host1.address == self.address:
                    target_switch = link.host2
                else:
                    target_switch = link.host1
                link.send_message_from_switch_to_switch(message, target_switch, host_list, start_time=start_time)

    def check_address_in_table(self, address):
        if address in self.mac_table:
            return True
        else:
            return False

    # def receive_message(self, message, link, host_list, switch_list, link_list, print_flag=False, start_time=0):
    #     answer = self.add_to_table(message.src_address, link, message, link_list, print_flag, start_time=start_time)
    #     if message.src_address in switch_list:
    #         self.receive_message_from_switch(message, link, host_list, link_list, print_flag=print_flag,
    #                                          start_time=start_time)
    #     target_host = host_list[message.dst_address]
    #     if answer == "flood":
    #         self.flooding(host_list, message, switch_list, start_time=start_time)
    #     else:
    #         link.send_message_from_switch(message, target_host, print_flag=False, start_time=start_time)

    def receive_message_part_2(self, message, link, destination_host_list, switch_list, link_list, print_flag=False,
                               curr_time=0):
        sending_host_id = message.src_address
        target_host_id = message.dst_address
        answer = self.add_to_table(message.src_address, link, message, link_list, print_flag=print_flag,
                                   curr_time=curr_time)
        if answer == "flood":
            self.flooding_part_2(destination_host_list, message, curr_time=curr_time)
        else:  # dst host is known to switch
            if self.queue_type == "input":
                self.switch_queues[sending_host_id].appendleft(message)
            elif self.queue_type == "output":

                self.switch_queues[target_host_id - destination_host_list[0].address].appendleft(message)
            else:  # virtual
                self.switch_queues[message.src_address][message.dst_address - len(self.switch_queues)].appendleft(
                    message)

    def receive_message_part_3(self, message, link, destination_host_list, switch_list, link_list, print_flag=False,
                               curr_time=0):
        sending_host_id = message.src_address
        target_host_id = message.dst_address
        self.packets_rec+=1
        answer = self.add_to_table(message.src_address, link, message, link_list, print_flag=print_flag,
                                   curr_time=curr_time)
        if answer == "flood":
            self.flooding_part_2(destination_host_list, message, curr_time=curr_time)
        else:
            if print_flag:# dst host is known to switch
                print(f'switch received message at time{curr_time}')
            if self.scheduling_algorithm == "fifo":
                self.switch_queues[0].append(message)
            elif self.scheduling_algorithm == "priority":
                self.switch_queues[0].append(message)
                temp_list = list(self.switch_queues[0])
                temp_list.sort(key=lambda x: (x.src_address, x.schedule_time, x.message_id), reverse=False)
                self.switch_queues[0] = deque(temp_list)
            elif self.scheduling_algorithm == "pgps":
                self.switch_queues[0].append(message)
                # print(f'curr time is {curr_time}, message scheduling time is{message.schedule_time}')
                self.switch_queues[0] = deque(self.find_gps_ending_times(link,curr_time))

    def find_gps_ending_times(self, link,curr_time):
        gps_finish_times = Scheduling.run_gps_for_messages(self.switch_queues[0], link.transmission_rate,curr_time)
        pgps_queue = gps_finish_times
        return pgps_queue


    def flooding_part_2(self, destination_host_list, message, curr_time):
        for dst_host in destination_host_list:
            new_message = Message.Message(message.message_id, message.src_address, dst_host.address,
                                          message.message_size, message.start_time, message.message_type)

            if self.queue_type == "input":
                self.switch_queues[new_message.src_address].appendleft(new_message)
            elif self.queue_type == "output":
                self.switch_queues[new_message.dst_address - destination_host_list[0].address].appendleft(new_message)
            else:  # virtual
                self.switch_queues[new_message.src_address][dst_host.address - len(self.switch_queues)].appendleft(
                    new_message)

    def receive_message_from_switch(self, message, link, host_list, link_list, print_flag=False, start_time=0):
        answer = self.add_to_table(message.src_address, link, message, link_list, print_flag=print_flag,
                                   curr_time=start_time)
        target_host = host_list[message.dst_address]
        if answer == "flood":
            self.flooding(host_list, message, start_time=start_time)
        else:
            link.send_message_from_switch(message, target_host, print_flag=False, start_time=start_time)

    def get_port_by_message(self, message):
        for entry in self.mac_table:
            if entry[1] == message.get_msg_src_mac():
                return entry[2]
        return None

    def send_message_to_host_part_2(self, message, link_list, host_list, curr_time, print_flag=False):
        arriving_link = [link for link in link_list if link.host1.address == message.src_address][0]
        curr_queue = self.switch_queues[message.src_address]
        answer = self.add_to_table(message.src_address, arriving_link, message, link_list, print_flag,
                                   curr_time=curr_time)
        if answer == "flood":
            valid_hosts = [host for host in host_list if host.address != message.src_address]
            curr_message = curr_queue.pop(0)
            for target_host in valid_hosts:
                curr_link = [link for link in link_list if link.host1 == target_host][0]

                curr_message.dst_address = target_host.address
                if not curr_link.is_link_busy(curr_time, message.message_size):
                    curr_link.send_message_from_switch_part_2(message, target_host, print_flag, curr_time)
                    curr_link.time_sent = curr_time

                else:  # link is busy
                    if self.switch_queues == 'input':
                        self.switch_queues[curr_message.src_address].insert(0, curr_message)
                    elif self.queue_type == 'output':
                        self.switch_queues[curr_message.dst_address - host_list[0].address].insert(0, curr_message)
                    else:  # virtual
                        self.switch_queues[curr_message.src_address][
                            curr_message.dst_address - len(self.switch_queues)].insert(0, curr_message)
                    return -1

        else:  # dst host is known to switch
            output_link = [link for link in link_list if link.host1.address == message.dst_address][0]
            if not output_link.is_link_busy(curr_time, message.message_size):
                output_link.send_message_from_switch_part_2(message, host_list[message.dst_address], print_flag,
                                                            curr_time)
                output_link.time_sent = curr_time
                curr_queue.pop(0)

    def start_hol_blocking(self, blocking_message, blocked_queue, curr_time):
        if self.queue_type == "input" or self.queue_type == "output":
            second_message_to_send = None
            blocked_queue_number = self.switch_queues.index(blocked_queue)

            for queue in self.switch_queues:
                if blocked_queue == queue:
                    continue
                else:
                    for message in queue:
                        if second_message_to_send is None or message.schedule_time < second_message_to_send.schedule_time:
                            second_message_to_send = message
            if second_message_to_send is not None:
                for message in blocked_queue:
                    if message != blocking_message:
                        if (message.schedule_time <= second_message_to_send.schedule_time
                                and message.dst_address != blocking_message.dst_address):
                            self.hol_blockers[blocked_queue_number] = [blocking_message, curr_time]

        else:  # virtual
            second_message_to_send = None
            blocked_queue_input_number = blocking_message.src_address
            blocked_queue_output_number = blocking_message.dst_address - len(self.switch_queues)
            for input_queue in self.switch_queues:
                for output_queue in input_queue:
                    if blocked_queue == output_queue:
                        continue
                    else:
                        for message in output_queue:
                            if second_message_to_send is None or message.schedule_time < second_message_to_send.schedule_time:
                                second_message_to_send = message
            if second_message_to_send is not None:
                for message in blocked_queue:
                    if message != blocking_message:
                        if message.schedule_time <= second_message_to_send.schedule_time and message.dst_address != blocking_message.dst_address:
                            self.hol_blockers[blocked_queue_input_number][blocked_queue_output_number] = [
                                blocking_message, curr_time]

    def calc_hol_blocking(self, blocking_message, blocked_queue, curr_time):
        if self.queue_type == "input" or self.queue_type == "output":
            blocked_queue_number = self.switch_queues.index(blocked_queue)
            if self.hol_blockers[blocked_queue_number] != [0, 0] and self.hol_blockers[blocked_queue_number][
                0] != blocking_message:
                self.total_hol_time += curr_time - self.hol_blockers[blocked_queue_number][1]
                self.hol_blockers[blocked_queue_number] = [0, 0]
        else:  # virtual
            blocked_queue_input_number = blocking_message.src_address
            blocked_queue_output_number = blocking_message.dst_address - len(self.switch_queues)
            if self.hol_blockers[blocked_queue_input_number][blocked_queue_output_number] != [0, 0] \
                    and self.hol_blockers[blocked_queue_input_number][blocked_queue_output_number][
                0] != blocking_message:
                self.total_hol_time += curr_time - \
                                       self.hol_blockers[blocked_queue_input_number][blocked_queue_output_number][1]
                self.hol_blockers[blocked_queue_input_number][blocked_queue_output_number] = [0, 0]

    def find_next_top_message(self, queues, old_queue):
        top_of_queues = []
        for i in range(len(queues)):
            if i == old_queue:
                continue
            else:
                if len(queues[i]) > 0:
                    top_of_queues.append(queues[i][0])
        top_of_queues.sort(key=lambda x: x.schedule_time)
        return top_of_queues

    def print_mac_table(self, link_list):
        print(f"\nMAC Table for switch {self.address}:\n")
        print("Used | Addr. | Port  | TTL")
        for entry in self.mac_table:
            if entry is None:
                print(f"{None} | {None}  | {None}  | {None}")
            else:
                print(f"{entry[0]} |   {entry[1]}   |"
                      f"   {link_list.index(entry[2])}    | {entry[3]} ")
        print("\n")

    def get_id(self):
        return self.address

    def is_queue_empty(self):
        return len(self.switch_queues[0])==0
