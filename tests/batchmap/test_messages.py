import unittest

from pynumaflow.batchmapper import BatchResponse, BatchResponses
from pynumaflow.batchmapper import Message, DROP
from tests.testing_utils import mock_message


class TestBatchResponse(unittest.TestCase):
    def test_invalid_create(self):
        with self.assertRaises(TypeError):
            BatchResponse.new_batch_response()

    def test_id(self):
        msg = BatchResponse.new_batch_response("4")
        self.assertEqual("4", msg.id())

    def test_append(self):
        mock_obj = {"Keys": ["test-key"], "Value": mock_message()}
        batch_response = BatchResponse.new_batch_response("4")
        msg = Message(value=mock_obj["Value"], keys=mock_obj["Keys"])
        batch_response.append(msg)
        self.assertEqual(1, len(batch_response.items()))


class TestBatchResponses(unittest.TestCase):
    def test_append(self):
        mock_obj = {"Keys": ["test-key"], "Value": mock_message()}
        batch_response = BatchResponse.new_batch_response("4")
        msg = Message(value=mock_obj["Value"], keys=mock_obj["Keys"])
        batch_response.append(msg)
        batch_responses = BatchResponses()
        batch_responses.append(batch_response)
        self.assertEqual(1, len(batch_responses.items()))


class TestMessage(unittest.TestCase):
    def test_key(self):
        mock_obj = {"Keys": ["test-key"], "Value": mock_message()}
        msg = Message(value=mock_obj["Value"], keys=mock_obj["Keys"])
        print(msg)
        self.assertEqual(mock_obj["Keys"], msg.keys)

    def test_value(self):
        mock_obj = {"Keys": ["test-key"], "Value": mock_message()}
        msg = Message(value=mock_obj["Value"], keys=mock_obj["Keys"])
        self.assertEqual(mock_obj["Value"], msg.value)

    def test_message_to_all(self):
        mock_obj = {"Keys": [], "Value": mock_message(), "Tags": []}
        msg = Message(mock_obj["Value"])
        self.assertEqual(Message, type(msg))
        self.assertEqual(mock_obj["Keys"], msg.keys)
        self.assertEqual(mock_obj["Value"], msg.value)
        self.assertEqual(mock_obj["Tags"], msg.tags)

    def test_message_to_drop(self):
        mock_obj = {"Keys": [], "Value": b"", "Tags": [DROP]}
        msg = Message(b"").to_drop()
        self.assertEqual(Message, type(msg))
        self.assertEqual(mock_obj["Keys"], msg.keys)
        self.assertEqual(mock_obj["Value"], msg.value)
        self.assertEqual(mock_obj["Tags"], msg.tags)

    def test_message_to(self):
        mock_obj = {"Keys": ["__KEY__"], "Value": mock_message(), "Tags": ["__TAG__"]}
        msg = Message(value=mock_obj["Value"], keys=mock_obj["Keys"], tags=mock_obj["Tags"])
        self.assertEqual(Message, type(msg))
        self.assertEqual(mock_obj["Keys"], msg.keys)
        self.assertEqual(mock_obj["Value"], msg.value)
        self.assertEqual(mock_obj["Tags"], msg.tags)


if __name__ == "__main__":
    unittest.main()
