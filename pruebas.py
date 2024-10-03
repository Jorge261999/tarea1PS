import unittest
import grpc
import distance_unary_pb2_grpc as pb2_grpc
import distance_unary_pb2 as pb2
from google.protobuf.json_format import MessageToJson

class TestGeodesicDistance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configuración del canal gRPC antes de todas las pruebas
        cls.channel = grpc.insecure_channel("localhost:50051")
        cls.stub = pb2_grpc.DistanceServiceStub(cls.channel)

    @classmethod
    def tearDownClass(cls):
        # Cierra el canal gRPC después de todas las pruebas
        cls.channel.close()

    def test_valid_coordinates_and_unit(self):
        message = pb2.SourceDest(
            source=pb2.Position(
                latitude=-33.0351516, longitude=-70.5955963
            ),
            destination=pb2.Position(
                latitude=-33.0348327, longitude=-71.5980458
            ),
            unit="km"
        )
        
        response = self.stub.geodesic_distance(message)

        expected_distance = 93.6  # Ajusta este valor a lo que esperas según el cálculo real
        self.assertAlmostEqual(response.distance, expected_distance, delta=0.1)

    def test_invalid_unit(self):
        message = pb2.SourceDest(
            source=pb2.Position(
                latitude=-33.0351516, longitude=-70.5955963
            ),
            destination=pb2.Position(
                latitude=-33.0348327, longitude=-71.5980458
            ),
            unit="invalid_unit"  # Unidad no válida para el test
        )

        with self.assertRaises(grpc.RpcError) as cm:
            self.stub.geodesic_distance(message)
        
        self.assertEqual(cm.exception.code(), grpc.StatusCode.INVALID_ARGUMENT)

if __name__ == "__main__":
    unittest.main()
