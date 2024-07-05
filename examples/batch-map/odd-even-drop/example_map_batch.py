import os
import json
import base64
from collections.abc import AsyncIterable
from pynumaflow.batchmapper import Message, Messages, Datum, BatchMapper, BatchMapServer, BatchResponses

import numpy as np

SLEEP_TIME = int(os.environ.get("SLEEP_TIME_SEC", "1"))

def b64_to_array(b64_data):
    data_bytes = base64.b64decode(b64_data)
    return np.frombuffer(data_bytes, dtype=np.uint8) * 1.0j

class MapperStreamer(BatchMapper):

    async def handler(self, datum: AsyncIterable[Datum]) -> AsyncIterable[BatchResponses]:
        """
        A handler to iterate over each item in stream and will output message for each item.
        For example, indicates even, odd, or DROP if 0.

        This will sleep a very short time to simulate longer processing so that we can see
        messages actually backing up and getting fetched and processed in batches
        """
        all_grouped = []

        async for msg in datum:

            parsed = json.loads(msg.value.decode())
            val = hash(parsed["Data"]["padding"])
            base64.b64decode(parsed["Data"]["padding"])
            
            as_str = str(val)
            all_grouped.append(val)
            # print(f"Computed message value = {as_str}")

            last_int = int(as_str[-1])
            if last_int == 0:
                yield BatchResponses.to_drop(msg.id)
                continue

            if last_int % 2 == 0:
                output_keys = ["even"]
                output_tags = ["even-tag"]
            else:
                output_keys = ["odd"]
                output_tags = ["odd-tag"]

            msgs = Messages(
                Message(value=as_str.encode("utf-8"), keys=output_keys, tags=output_tags)
            )
            response = BatchResponses(msg.id, msgs)
            # print(f"Returning {response}")
            yield response

if __name__ == "__main__":
    # NOTE: stream handler does currently support function-only handler
    print("Stream")
    handler = MapperStreamer()
    grpc_server = BatchMapServer(handler)
    grpc_server.start()