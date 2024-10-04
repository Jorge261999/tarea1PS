import unittest
import grpc
import distance_unary_pb2_grpc as pb2_grpc
import distance_unary_pb2 as pb2

class TestDistanceService(unittest.TestCase):  # Clase de prueba

    def setUp(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = pb2_grpc.DistanceServiceStub(self.channel)

    def test_geodesic_distance_valid(self):
        # Test case 1: Cordinadas validas
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-90, longitude=-180), 
            destination=pb2.Position(latitude=90, longitude=180), 
            unit="km"
        )
        response = self.stub.geodesic_distance(message)
        self.assertAlmostEqual(response.distance, 20003.8, delta=1, msg="Test case 1 failed!")
        print("Test case 1 passed!")  

    def test_geodesic_distance_invalid_latitude(self):
        # Test case 2: Latitud fuera de rango
        message_invalid = pb2.SourceDest(
            source=pb2.Position(latitude=100, longitude=-180), 
            destination=pb2.Position(latitude=90, longitude=180), 
            unit="km"
        )

        with self.assertRaises(ValueError):
            self.stub.geodesic_distance(message_invalid)
        print("Test case 2 passed!")  

    def test_geodesic_distance_invalid_longitude(self):
        # Test case 3: Longitud fuera de rango
        message_invalid = pb2.SourceDest(
            source=pb2.Position(latitude=-90, longitude=-181), 
            destination=pb2.Position(latitude=90, longitude=180), 
            unit="km"
        )

        with self.assertRaises(ValueError):
            self.stub.geodesic_distance(message_invalid)
        print("Test case 3 passed!")  

    def test_geodesic_distance_valid_same_point(self):
        # Test case 4: Coordenada validas, mismo punto con "nm"
        message = pb2.SourceDest(
            source=pb2.Position(latitude=90, longitude=180), 
            destination=pb2.Position(latitude=90, longitude=180), 
            unit="nm"
        )
        response = self.stub.geodesic_distance(message)
        print(f"Server response: {response}")
        self.assertAlmostEqual(response.distance, 0, delta=0.1, msg="Expected distance to be 0 for the same point!")
        self.assertEqual(response.unit, "nm", msg="Expected unit to be 'nm'!")
        print("Test case 4 passed: distance is 0 for the same point.")

    def test_geodesic_distance_invalid_latitude_type(self):
        # Test case 5: Latitud invalida, string
        with self.assertRaises(TypeError, msg="Expected TypeError for invalid latitude type!"):
            message = pb2.SourceDest(
                source=pb2.Position(latitude="invalid", longitude=180),  
                destination=pb2.Position(latitude=90, longitude=180), 
                unit="km"
            )

            response = self.stub.geodesic_distance(message)

        print("Test case 5 passed: TypeError raised for invalid latitude type.")

    def test_geodesic_distance_invalid_unit(self):
        # Test case 6: Unidad invalida "metros"
        with self.assertRaises(ValueError, msg="Expected ValueError for invalid unit 'metros'!"):
            message = pb2.SourceDest(
                source=pb2.Position(latitude=-90, longitude=-180), 
                destination=pb2.Position(latitude=90, longitude=180), 
                unit="metros"  
            )

            response = self.stub.geodesic_distance(message)
    
        print("Test case 6 passed: ValueError raised for invalid unit 'metros'.")

    def test_geodesic_distance_empty_unit(self):
        # Test case 7: Coordinadas validas pero unidad vacia
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-80, longitude=-170), 
            destination=pb2.Position(latitude=80, longitude=170), 
            unit=""  
        )
    
        response = self.stub.geodesic_distance(message)
    
        self.assertEqual(response.unit, "km", 
                        msg=f"Test case failed! Expected default unit 'km' but got '{response.unit}' instead.\n-----Response-----\nDistance: {response.distance}\nMethod: geodesic\nDistance unit: {response.unit}")

        expected_distance = 17804
        self.assertAlmostEqual(response.distance, expected_distance, delta=1, 
                            msg=f"Test case failed! Expected distance {expected_distance}, but got {response.distance} instead.\n-----Response-----\nDistance: {response.distance}\nMethod: geodesic\nDistance unit: {response.unit}")
    
        print(f"Test case 7 passed: Empty unit correctly defaults to 'km' and distance is {response.distance}.")


# Run the tests
if __name__ == "__main__":
    unittest.main(exit=False)  
