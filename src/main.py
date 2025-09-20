import os
import sys
import asyncio

sys.path.insert(1, os.path.join(sys.path[0], ".."))


from queries.core import SyncCore


SyncCore.create_tables()
SyncCore.select_workers()
