from IPython.kernel import client
mec = client.MultiEngineClient()
print mec.get_ids()
