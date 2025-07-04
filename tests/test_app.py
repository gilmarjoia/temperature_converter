import unittest
import json
from app import app

class TestTemperatureAPI(unittest.TestCase):
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True

    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['message'], 'Temperature conversion API is working')

    def test_celsius_to_fahrenheit_valid(self):
        """Test Celsius to Fahrenheit conversion with valid data"""
        test_data = {'temperature': 25}
        response = self.app.post('/convert/celsius-to-fahrenheit',
                               data=json.dumps(test_data),
                               content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['celsius'], 25)
        self.assertEqual(data['fahrenheit'], 77.0)
        self.assertEqual(data['message'], '25°C = 77.0°F')

    def test_fahrenheit_to_celsius_valid(self):
        """Test Fahrenheit to Celsius conversion with valid data"""
        test_data = {'temperature': 77}
        response = self.app.post('/convert/fahrenheit-to-celsius',
                               data=json.dumps(test_data),
                               content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['fahrenheit'], 77)
        self.assertEqual(data['celsius'], 25.0)
        self.assertEqual(data['message'], '77°F = 25.0°C')

    def test_generic_convert_celsius_to_fahrenheit(self):
        """Test generic conversion endpoint - Celsius to Fahrenheit"""
        test_data = {
            'temperature': 25,
            'from_unit': 'celsius',
            'to_unit': 'fahrenheit'
        }
        response = self.app.post('/convert',
                               data=json.dumps(test_data),
                               content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['temperature'], 25)
        self.assertEqual(data['from_unit'], 'celsius')
        self.assertEqual(data['to_unit'], 'fahrenheit')
        self.assertEqual(data['result'], 77.0)
        self.assertEqual(data['message'], '25°C = 77.0°F')

    def test_generic_convert_fahrenheit_to_celsius(self):
        """Test generic conversion endpoint - Fahrenheit to Celsius"""
        test_data = {
            'temperature': 77,
            'from_unit': 'fahrenheit',
            'to_unit': 'celsius'
        }
        response = self.app.post('/convert',
                               data=json.dumps(test_data),
                               content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['temperature'], 77)
        self.assertEqual(data['from_unit'], 'fahrenheit')
        self.assertEqual(data['to_unit'], 'celsius')
        self.assertEqual(data['result'], 25.0)
        self.assertEqual(data['message'], '77°F = 25.0°C')

    def test_api_info_endpoint(self):
        """Test API information endpoint"""
        response = self.app.get('/')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'Temperature Conversion API')
        self.assertEqual(data['version'], '1.0.0')
        self.assertIn('endpoints', data)

    def test_missing_temperature_field(self):
        """Test error handling for missing temperature field"""
        test_data = {}
        response = self.app.post('/convert/celsius-to-fahrenheit',
                               data=json.dumps(test_data),
                               content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Field "temperature" is required')

    def test_invalid_temperature_type(self):
        """Test error handling for invalid temperature type"""
        test_data = {'temperature': 'invalid'}
        response = self.app.post('/convert/celsius-to-fahrenheit',
                               data=json.dumps(test_data),
                               content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Temperature must be a number')

    def test_unsupported_unit_combination(self):
        """Test error handling for unsupported unit combination"""
        test_data = {
            'temperature': 25,
            'from_unit': 'celsius',
            'to_unit': 'celsius'
        }
        response = self.app.post('/convert',
                               data=json.dumps(test_data),
                               content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('Unsupported unit combination', data['error'])

    def test_edge_cases(self):
        """Test edge cases for temperature conversions"""
        # Test 0°C
        test_data = {'temperature': 0}
        response = self.app.post('/convert/celsius-to-fahrenheit',
                               data=json.dumps(test_data),
                               content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data['fahrenheit'], 32.0)
        
        # Test 100°C
        test_data = {'temperature': 100}
        response = self.app.post('/convert/celsius-to-fahrenheit',
                               data=json.dumps(test_data),
                               content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data['fahrenheit'], 212.0)
        
        # Test negative temperatures
        test_data = {'temperature': -40}
        response = self.app.post('/convert/celsius-to-fahrenheit',
                               data=json.dumps(test_data),
                               content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data['fahrenheit'], -40.0)

    def test_decimal_precision(self):
        """Test decimal precision in conversions"""
        test_data = {'temperature': 37.5}
        response = self.app.post('/convert/celsius-to-fahrenheit',
                               data=json.dumps(test_data),
                               content_type='application/json')
        data = json.loads(response.data)
        
        # 37.5°C should be 99.5°F
        self.assertEqual(data['fahrenheit'], 99.5)

if __name__ == '__main__':
    unittest.main() 