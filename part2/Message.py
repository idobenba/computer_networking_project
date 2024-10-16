class Message:
    def __init__(self, message_id, src_address, dst_address, message_size,schedule_time,
                 start_time, message_type="Data"):
        self.message_id = message_id
        self.message_type = message_type
        self.src_address = src_address
        self.dst_address = dst_address
        self.message_size = message_size
        self.schedule_time = schedule_time
        self.Mac_time = 0
        self.start_time = start_time

    def get_msg_src_mac(self):
        return self.src_address

    def get_mac_time(self):
        return self.Mac_time

    def update_message(self, message_id, dst_address):
        self.message_id = message_id
        self.dst_address = dst_address
