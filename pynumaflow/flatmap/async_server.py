import os

import aiorun
import grpc
from grpc import experimental

from pynumaflow.mapstreamer.servicer.async_servicer import AsyncMapStreamServicer
from pynumaflow.proto.flatmap import flatmap_pb2_grpc

from pynumaflow._constants import (
    FLAT_MAP_SOCK_PATH,
    MAX_MESSAGE_SIZE,
    MAX_THREADS,
    _LOGGER,
    FLAT_MAP_SERVER_INFO_FILE_PATH,
)

from pynumaflow.mapstreamer._dtypes import MapStreamCallable

from pynumaflow.shared.server import NumaflowServer, start_async_server


class FlatmapAsyncServer(NumaflowServer):
    """
    Class for a new Map Stream Server instance.
    """

    def __init__(
        self,
        map_stream_instance: MapStreamCallable,
        sock_path=FLAT_MAP_SOCK_PATH,
        max_message_size=MAX_MESSAGE_SIZE,
        max_threads=MAX_THREADS,
        server_info_file=FLAT_MAP_SERVER_INFO_FILE_PATH,
        servicer_class=AsyncMapStreamServicer,
    ):
        """
        Create a new grpc Async Map Stream Server instance.
        A new servicer instance is created and attached to the server.
        The server instance is returned.
        Args:
            map_stream_instance: The map stream instance to be used for Map Stream UDF
            sock_path: The UNIX socket path to be used for the server
            max_message_size: The max message size in bytes the server can receive and send
            max_threads: The max number of threads to be spawned;
                            defaults to number of processors x4
            server_type: The type of server to be used

        Example invocation:
            import os
            from collections.abc import AsyncIterable
            from pynumaflow.mapstreamer import Message, Datum, MapStreamAsyncServer, MapStreamer

            class FlatMapStream(MapStreamer):
                async def handler(self, keys: list[str], datum: Datum) -> AsyncIterable[Message]:
                    val = datum.value
                    _ = datum.event_time
                    _ = datum.watermark
                    strs = val.decode("utf-8").split(",")

                    if len(strs) == 0:
                        yield Message.to_drop()
                        return
                    for s in strs:
                        yield Message(str.encode(s))

            async def map_stream_handler(_: list[str], datum: Datum) -> AsyncIterable[Message]:

                val = datum.value
                _ = datum.event_time
                _ = datum.watermark
                strs = val.decode("utf-8").split(",")

                if len(strs) == 0:
                    yield Message.to_drop()
                    return
                for s in strs:
                    yield Message(str.encode(s))

            if __name__ == "__main__":
                invoke = os.getenv("INVOKE", "func_handler")
                if invoke == "class":
                    handler = FlatMapStream()
                else:
                    handler = map_stream_handler
                grpc_server = MapStreamAsyncServer(handler)
                grpc_server.start()

        """
        self.map_stream_instance: MapStreamCallable = map_stream_instance
        self.sock_path = f"unix://{sock_path}"
        self.max_threads = min(max_threads, int(os.getenv("MAX_THREADS", "4")))
        self.max_message_size = max_message_size
        self.server_info_file = server_info_file

        self._server_options = [
            ("grpc.max_send_message_length", self.max_message_size),
            ("grpc.max_receive_message_length", self.max_message_size),
        ]

        self.servicer = servicer_class(handler=self.map_stream_instance)

    def start(self):
        """
        Starter function for the Async Map Stream server, we need a separate caller
        to the aexec so that all the async coroutines can be started from a single context
        """
        print("MDW: Calling FlatmapAsyncServer.start")
        aiorun.run(self.aexec(), use_uvloop=True)

    async def aexec(self):
        """
        Starts the Async gRPC server on the given UNIX socket with
        given max threads.
        """
        # As the server is async, we need to create a new server instance in the
        # same thread as the event loop so that all the async calls are made in the
        # same context
        # Create a new async server instance and add the servicer to it
        print("MDW: grpc.aio.server")
        server = grpc.aio.server()
        print(f"MDW: {self.sock_path}")
        server.add_insecure_port(self.sock_path)
        print(f"MDW: add_MapStreamServicer_to_server")
        flatmap_pb2_grpc.add_FlatmapServicer_to_server(
            self.servicer,
            server,
        )
        _LOGGER.info("Starting Flatmap Server")
        print("MDW: Starting Flatmap Server")
        await start_async_server(
            server, self.sock_path, self.max_threads, self._server_options, self.server_info_file
        )
