from client.CMCClient import CMCClientImpl
from client.Client import registerClient

clientInstance = CMCClientImpl()

registerClient(clientInstance)
