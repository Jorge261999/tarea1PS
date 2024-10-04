import unittest
import grpc
import distance_unary_pb2_grpc as pb2_grpc
import distance_unary_pb2 as pb2

class TestDistanceService(unittest.TestCase):  # Clase de prueba

    def setUp(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = pb2_grpc.DistanceServiceStub(self.channel)

    def test_geodesic_distance_valid(self):
        # Test case 1: Valid coordinates
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-90, longitude=-180), 
            destination=pb2.Position(latitude=90, longitude=180), 
            unit="km"
        )
        response = self.stub.geodesic_distance(message)
        self.assertAlmostEqual(response.distance, 20015, delta=0.1, msg="Test case 1 failed!")
        print("Test case 1 passed!")  # Mensaje de éxito para el primer test

    def test_geodesic_distance_invalid(self):
        # Test case 2: Invalid coordinates
        message_invalid = pb2.SourceDest(
            source=pb2.Position(latitude=100, longitude=-180), 
            destination=pb2.Position(latitude=90, longitude=180), 
            unit="km"
        )
        # Expect ValueError to be raised
        with self.assertRaises(ValueError):
            self.stub.geodesic_distance(message_invalid)
        print("Test case 2 passed!")  # Mensaje de éxito para el segundo test

# Run the tests
if __name__ == "__main__":
    unittest.main(exit=False)  # `exit=False` evita que el script termine al final de las pruebas
