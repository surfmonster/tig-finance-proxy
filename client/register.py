from client.cmc_client import CMCClientImpl
from client.client import register_client

clientInstance = CMCClientImpl()


def register_all():
    register_client(clientInstance)
