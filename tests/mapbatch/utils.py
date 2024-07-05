from pynumaflow.batchmapper import Datum
from pynumaflow.proto.batchmapper import batchmap_pb2
from tests.testing_utils import get_time_args, mock_message


def generate_request_item(msg_id) -> batchmap_pb2.BatchMapRequest:
    event_time_timestamp, watermark_timestamp = get_time_args()
    
    request = batchmap_pb2.BatchMapRequest(
        value=mock_message(),
        event_time=event_time_timestamp,
        watermark=watermark_timestamp,
        id=msg_id,
    )

    yield request
