from pypresence import Presence
import time

client_id = "736398384226762763"
RPC = Presence(client_id)
RPC.connect()
RPC.update(start=6, state="Version 0.0.3", details="Destroying Zalando", large_image="test", small_image="start")
RPC.clear()
RPC.close()


