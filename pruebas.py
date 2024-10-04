import unittest
import grpc
import distance_unary_pb2_grpc as pb2_grpc
import distance_unary_pb2 as pb2

class TestDistanceService(unittest.TestCase):  # Clase de prueba

    def test_geodesic_distance(self):
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = pb2_grpc.DistanceServiceStub(channel)

            # Test case 1: Valid coordinates
            message = pb2.SourceDest(
                source=pb2.Position(latitude=-90, longitude=-180), 
                destination=pb2.Position(latitude=90, longitude=180), 
                unit="km"
            )
            response = stub.geodesic_distance(message)
            self.assertAlmostEqual(response.distance, 20015, delta=0.1, msg="Test case 1 failed!")

# Run the tests
if __name__ == "__main__":
    unittest.main()
