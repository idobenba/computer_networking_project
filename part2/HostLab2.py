import Host

class HostLab2(Host):
    def __init__(self, address, nic, object_id,host_list):
        super().__init__(address, nic, object_id)
        self.host_list = [host for host in host_list if host.address != self.address]
