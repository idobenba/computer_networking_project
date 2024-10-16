class Packet:
    def __init__(self, packet_number, size, arrival_time, priority):
        self.packet_number = packet_number
        self.size = size
        self.arrival_time = arrival_time
        self.priority = float(priority)
        self.start_time = None
        self.end_time = None
        self.remaining_size = size
        self.rate = 0
        self.wait = False

    def __lt__(self, other):
        if self.arrival_time == other.arrival_time:
            return self.priority > other.priority
        return self.arrival_time < other.arrival_time


def cast_messages_to_packets(messages):
    packets = []
    for message in messages:
        packet = Packet(message.message_id, message.message_size, message.schedule_time, message.priority)
        packets.append(packet)
    return packets


def simulate_gps(packets, transmission_rate,curr_time=0):
    # curr_time = 0
    gps_queue = []
    timeline = []

    if len(packets)>1 :
        while packets or gps_queue:  # Continue until all packets have been sent
            # Add arriving packets to the GPS queue
            while packets and packets[0].arrival_time <= curr_time:  # adding packets that arrived
                packet = packets.pop(0)
                for p in gps_queue:  # check packets with same priority
                    if abs(p.priority - packet.priority)==0:
                        packet.wait = True
                if not packet.wait:
                    packet.start_time = curr_time
                    # if packet.start_time is None:
                    #     print("hello")
                if packet.wait==False:
                    gps_queue.append(packet)
            # for packet in packets:
                # if packet.start_time is None:
                #     print("hello")

            if not gps_queue:  # If there are no packets in the GPS queue
                curr_time = packets[0].arrival_time if packets \
                    else curr_time
                continue

            # Calculate total weight and determine minimum time to send a portion

            total_weight = sum(p.priority for p in gps_queue if not p.wait)
            # if total_weight == 0:
                # print("here")
            rate = [transmission_rate * (p.priority / total_weight) if not p.wait else 0 for p in
                    gps_queue]

            time_temp_1 = min(p.arrival_time for p in packets) if packets \
                else float('inf')
            time_temp_1=float('inf')
            time_temp_2= curr_time+ min(p.size / r for p, r in zip(gps_queue, rate) if r > 0)
            next_event_time = min(time_temp_1,time_temp_2)

            # Move time forward to the next event
            curr_time = next_event_time

            # Update packet sizes and check for finished packets
            finished_packets = []
            for packet, r in zip(gps_queue, rate):
                if packet.start_time is None and r>0:
                    print(f'packet with start time none is:{packet}')
                if r > 0:
                    down = packet.size - (r * (
                            curr_time - packet.start_time))
                    # down = round(down, 10)
                    packet.size = down
                    packet.start_time = curr_time
                    if packet.size <= 1e-6:
                        packet.end_time = curr_time
                        timeline.append(packet)
                        gps_queue.remove(packet)
                        finished_packets.append(packet)

                        # Remove finished packets from gps_queue
            for packet in finished_packets:
                # gps_queue.remove(packet)
                for q in gps_queue:
                    if q.priority == packet.priority:
                        q.wait = False
                        q.start_time = curr_time
                        # if packet.start_time is None:
                        #     print("hello")

                        # Sort timeline by packet number and print in the required format
        timeline.sort(key=lambda x: x.end_time)  # Sort the timeline by end time
    else:
        return packets
    return timeline



def run_gps_for_messages(messages, transmission_rate,curr_time):
    packets = cast_messages_to_packets(messages)
    finish_times = simulate_gps(packets, transmission_rate,curr_time)
    final_queue = []
    for i in range(len(finish_times)):
        for j in range(len(messages)):
            if finish_times[i].packet_number == messages[j].message_id:
                final_queue.append(messages[j])
                break
    return final_queue
