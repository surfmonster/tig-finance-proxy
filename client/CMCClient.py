from client.Client import ClientAbs, registerClient


class CMCClientImpl(ClientAbs):
    def __init__(self):
        super().__init__("CMC")



