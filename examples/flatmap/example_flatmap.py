import os
import sys
import time
import json
import base64
from collections.abc import AsyncIterable
# from pynumaflow.mapstreamer import Message, Datum, MapStreamAsyncServer
# from pynumaflow.mapstreamer.servicer.servicers import StreamFlatMap, StreamBatchMap
from pynumaflow.flatmap import Message, Datum, FlatmapAsyncServer
from pynumaflow.flatmap.servicer.servicers import FlatMapServer, FlatMapBatchMapServer

import numpy as np

SLEEP_TIME = int(os.environ.get("SLEEP_TIME_SEC", "1"))

def b64_to_array(b64_data):
    data_bytes = base64.b64decode(b64_data)
    return np.frombuffer(data_bytes, dtype=np.uint8) * 1.0j

class FlatmapHandler: #(StreamFlatMap):
    async def handler(self, keys: list[str], datum: Datum) -> AsyncIterable[Message]:
        parsed = json.loads(datum.value.decode())
        val = hash(parsed["Data"]["padding"])
        base64.b64decode(parsed["Data"]["padding"])
        
        as_str = str(val)
        # print(f"Computed message value = {as_str}")

        last_int = int(as_str[-1])
        if last_int == 0:
            # print(f"Drop {as_str}")
            yield Message.to_drop()

        if last_int % 2 == 0:
            output_keys = ["even"]
            output_tags = ["even-tag"]
        else:
            output_keys = ["odd"]
            output_tags = ["odd-tag"]
        yield Message(value=as_str.encode("utf-8"), keys=output_keys, tags=output_tags)    

    async def handler_stream(self, datum: AsyncIterable[Datum]) -> AsyncIterable[Message]:
        """
        A handler to iterate over each item in stream and will output message for each item.
        For example, indicates even, odd, or DROP if 0.

        This will sleep a very short time to simulate longer processing so that we can see
        messages actually backing up and getting fetched and processed in batches
        """
        all_grouped = []

        # Treat each message individually, because we can
        
        '''
        print(f"Simulate doing work for {SLEEP_TIME} sec")
        time.sleep(SLEEP_TIME)
        async for msg in datum:
            parsed = json.loads(msg.value.decode())
            val = hash(parsed["Data"]["padding"])
            base64.b64decode(parsed["Data"]["padding"])
            
            as_str = str(val)
            all_grouped.append(val)
            print(f"Computed message value = {as_str}")

            last_int = int(as_str[-1])
            if last_int == 0:
                print(f"Drop {as_str}")
                yield Message.to_drop()
                continue

            if last_int % 2 == 0:
                output_keys = ["even"]
                output_tags = ["even-tag"]
            else:
                output_keys = ["odd"]
                output_tags = ["odd-tag"]
            yield Message(value=as_str.encode("utf-8"), keys=output_keys, tags=output_tags)        

        # Show that we can do a messages separate from each individual one.
        # This demonstrates 'grouping' messages into fewer, but larger ,messages
        print(f"Group of {len(all_grouped)}")
        grouped_val = json.dumps(all_grouped).encode("utf-8")
        yield Message(value=grouped_val, tags=["grouped"])
        '''

        # Singular
        # print(f"{time.time():0.2f} Singular form")
        # async for msg in datum:
        #     parsed = json.loads(msg.value.decode())
        #     arr = b64_to_array(parsed["Data"]["padding"])
        #     result = np.fft.fft(arr)
        #     yield Message(value=result.tobytes(), tags=["grouped"])

        '''
        print(f"{time.time():0.2f} Mulitple form")
        batch = []
        # idx = 0
        async for msg in datum:
            # print(idx)
            # idx += 1
            parsed = json.loads(msg.value.decode())
            arr = b64_to_array(parsed["Data"]["padding"])
            batch.append(arr)

        result = np.fft.fft(np.array(batch))
        # print("Return group")
        yield Message(value=result.tobytes(), tags=["grouped"])
        '''

        
        async for msg in datum:
            parsed = json.loads(msg.value.decode())
            val = hash(parsed["Data"]["padding"])
            base64.b64decode(parsed["Data"]["padding"])
            
            as_str = str(val)
            all_grouped.append(val)
            # print(f"Computed message value = {as_str}")

            last_int = int(as_str[-1])
            if last_int == 0:
                # print(f"Drop {as_str}")
                yield Message.to_drop()
                continue

            if last_int % 2 == 0:
                output_keys = ["even"]
                output_tags = ["even-tag"]
            else:
                output_keys = ["odd"]
                output_tags = ["odd-tag"]
            yield Message(value=as_str.encode("utf-8"), keys=output_keys, tags=output_tags)    
        
        '''
        async for msg in datum:
            parsed = json.loads(msg.value.decode())
            val = hash(parsed["Data"]["padding"])
            base64.b64decode(parsed["Data"]["padding"])
            
            as_str = str(val)
            all_grouped.append(val)

        # Show that we can do a messages separate from each individual one.
        # This demonstrates 'grouping' messages into fewer, but larger ,messages
        print(f"Group of {len(all_grouped)}")
        grouped_val = json.dumps(all_grouped).encode("utf-8")
        yield Message(value=grouped_val, tags=["grouped"])
        '''


class StreamHandler:
    async def handler(self, datums: list[Datum]) -> AsyncIterable[Message]:
        # all_grouped = []
        # print(f"MDW: Handle batchsize = {len(datums)}")
        for msg in datums:
            parsed = json.loads(msg.value.decode())
            val = hash(parsed["Data"]["padding"])
            base64.b64decode(parsed["Data"]["padding"])
            
            as_str = str(val)
            # all_grouped.append(val)

            last_int = int(as_str[-1])
            if last_int == 0:
                # print(f"Drop {as_str}")
                yield Message.to_drop()
                continue

            if last_int % 2 == 0:
                output_keys = ["even"]
                output_tags = ["even-tag"]
            else:
                output_keys = ["odd"]
                output_tags = ["odd-tag"]
            yield Message(value=as_str.encode("utf-8"), keys=output_keys, tags=output_tags)        

        # Show that we can do a messages separate from each individual one.
        # This demonstrates 'grouping' messages into fewer, but larger ,messages
        # print(f"Group of {len(all_grouped)}")
        # grouped_val = json.dumps(all_grouped).encode("utf-8")
        # yield Message(value=grouped_val, tags=["grouped"])

if __name__ == "__main__":
    print(f"{sys.argv=}")
    if len(sys.argv) > 1:
        process_type = sys.argv[-1]

    if process_type == "flatmap":
        # NOTE: stream handler does currently support function-only handler
        print("StreamFlatMap")
        # handler = MapperStreamer()    
        # grpc_server = MapStreamAsyncServer(handler)

        handler = FlatmapHandler()
        servicer_class = FlatMapServer
        grpc_server = FlatmapAsyncServer(handler, servicer_class=servicer_class)
        grpc_server.start()
    elif process_type == "batch":
        print("BatchMap")
        
        handler = StreamHandler()
        servicer_class = FlatMapBatchMapServer
        grpc_server = FlatmapAsyncServer(handler, servicer_class=servicer_class)
        grpc_server.start()