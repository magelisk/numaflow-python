import asyncio
import logging
import threading
import unittest
from collections.abc import AsyncIterable

import grpc
from google.protobuf import empty_pb2 as _empty_pb2
from grpc.aio._server import Server

from pynumaflow import setup_logging
from pynumaflow.batchmapper import (
    BatchMapServer,
    Datum, 
    BatchResponses, 
    Message,
    Messages
)
from pynumaflow.proto.batchmapper import batchmap_pb2_grpc
from .utils import generate_request_item

# from pynumaflow.mapstreamer import (
#     Message,
#     Datum,
#     MapStreamAsyncServer,
# )
# from pynumaflow.proto.mapstreamer import mapstream_pb2_grpc
# from tests.mapstream.utils import start_request_map_stream

LOGGER = setup_logging(__name__)

# if set to true, map handler will raise a `ValueError` exception.
raise_error_from_map = False


async def async_batch_handler(datums: AsyncIterable[Datum]) -> AsyncIterable[BatchResponses]:
    idx = 0
    async for datum in datums:
        val = datum.value
        msg = "payload:{} event_time:{} watermark:{} id:{} idx:{}".format(
        val.decode("utf-8"),
        datum.event_time,
        datum.watermark,
        datum.id,
        idx,
    )
        msgs = Messages(Message(str.encode(msg), keys=[]))
        yield BatchResponses(datum.id, msgs)
        idx += 1
                    



_s: Server = None
_channel = grpc.insecure_channel("unix:///tmp/async_map_stream.sock")
_loop = None


def startup_callable(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def NewBatchMapStreamer(
    handler=async_batch_handler,
):
    server = BatchMapServer(mapper_instance=handler)
    udfs = server.servicer
    return udfs


async def start_server(udfs):
    server = grpc.aio.server()
    batchmap_pb2_grpc.add_BatchMapServicer_to_server(udfs, server)
    listen_addr = "unix:///tmp/async_map_stream.sock"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    global _s
    _s = server
    await server.start()
    await server.wait_for_termination()


class TestAsyncMapStreamer(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        global _loop
        loop = asyncio.new_event_loop()
        _loop = loop
        _thread = threading.Thread(target=startup_callable, args=(loop,), daemon=True)
        _thread.start()
        udfs = NewBatchMapStreamer()
        asyncio.run_coroutine_threadsafe(start_server(udfs), loop=loop)
        while True:
            try:
                with grpc.insecure_channel("unix:///tmp/async_map_stream.sock") as channel:
                    f = grpc.channel_ready_future(channel)
                    f.result(timeout=10)
                    if f.done():
                        break
            except grpc.FutureTimeoutError as e:
                LOGGER.error("error trying to connect to grpc server")
                LOGGER.error(e)

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            _loop.stop()
            LOGGER.info("stopped the event loop")
        except Exception as e:
            LOGGER.error(e)

    def test_map_stream(self) -> None:
        stub = self.__stub()
        # request = get_request_item("a")
        generator_response = None
        try:
            # generator_response = stub.BatchMapFn(request)
            generator_response = stub.BatchMapFn(request_iterator=generate_request_item("a"))
        except grpc.RpcError as e:
            logging.error(e)

        results = [x for x in generator_response]
        print(results)

        assert False, "for now"
#         counter = 0
#         # capture the output from the MapStreamFn generator and assert.
#         for r in generator_response:
#             counter += 1
#             self.assertEqual(
#                 bytes(
#                     "payload:test_mock_message "
#                     "event_time:2022-09-12 16:00:00 watermark:2022-09-12 16:01:00",
#                     encoding="utf-8",
#                 ),
#                 r.result.value,
#             )
#         """Assert that the generator was called 10 times in the stream"""
#         self.assertEqual(10, counter)

    def test_is_ready(self) -> None:
        with grpc.insecure_channel("unix:///tmp/async_map_stream.sock") as channel:
            stub = batchmap_pb2_grpc.BatchMapStub(channel)

            request = _empty_pb2.Empty()
            response = None
            try:
                response = stub.IsReady(request=request)
            except grpc.RpcError as e:
                logging.error(e)

            self.assertTrue(response.ready)

    def __stub(self):
        return batchmap_pb2_grpc.BatchMapStub(_channel)


# if __name__ == "__main__":
#     logging.basicConfig(level=logging.DEBUG)
#     unittest.main()
