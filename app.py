from flask import Flask, request, jsonify
from src.temperature_converter import celsius_to_fahrenheit, fahrenheit_to_celsius

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint to check if the API is working"""
    return jsonify({
        'status': 'healthy',
        'message': 'Temperature conversion API is working'
    }), 200

@app.route('/convert/celsius-to-fahrenheit', methods=['POST'])
def convert_celsius_to_fahrenheit():
    """Convert temperature from Celsius to Fahrenheit"""
    try:
        data = request.get_json()
        
        if not data or 'temperature' not in data:
            return jsonify({
                'error': 'Field "temperature" is required'
            }), 400
        
        temperature = data['temperature']
        
        if not isinstance(temperature, (int, float)):
            return jsonify({
                'error': 'Temperature must be a number'
            }), 400
        
        result = celsius_to_fahrenheit(temperature)
        
        return jsonify({
            'celsius': temperature,
            'fahrenheit': round(result, 2),
            'message': f'{temperature}°C = {round(result, 2)}°F'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/convert/fahrenheit-to-celsius', methods=['POST'])
def convert_fahrenheit_to_celsius():
    """Convert temperature from Fahrenheit to Celsius"""
    try:
        data = request.get_json()
        
        if not data or 'temperature' not in data:
            return jsonify({
                'error': 'Field "temperature" is required'
            }), 400
        
        temperature = data['temperature']
        
        if not isinstance(temperature, (int, float)):
            return jsonify({
                'error': 'Temperature must be a number'
            }), 400
        
        result = fahrenheit_to_celsius(temperature)
        
        return jsonify({
            'fahrenheit': temperature,
            'celsius': round(result, 2),
            'message': f'{temperature}°F = {round(result, 2)}°C'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/convert', methods=['POST'])
def convert_temperature():
    """Generic endpoint for temperature conversion"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'JSON data is required'
            }), 400
        
        temperature = data.get('temperature')
        from_unit = data.get('from_unit', '').lower()
        to_unit = data.get('to_unit', '').lower()
        
        if temperature is None:
            return jsonify({
                'error': 'Field "temperature" is required'
            }), 400
        
        if not isinstance(temperature, (int, float)):
            return jsonify({
                'error': 'Temperature must be a number'
            }), 400
        
        if from_unit == 'celsius' and to_unit == 'fahrenheit':
            result = celsius_to_fahrenheit(temperature)
            return jsonify({
                'temperature': temperature,
                'from_unit': 'celsius',
                'to_unit': 'fahrenheit',
                'result': round(result, 2),
                'message': f'{temperature}°C = {round(result, 2)}°F'
            }), 200
        
        elif from_unit == 'fahrenheit' and to_unit == 'celsius':
            result = fahrenheit_to_celsius(temperature)
            return jsonify({
                'temperature': temperature,
                'from_unit': 'fahrenheit',
                'to_unit': 'celsius',
                'result': round(result, 2),
                'message': f'{temperature}°F = {round(result, 2)}°C'
            }), 200
        
        else:
            return jsonify({
                'error': 'Unsupported unit combination. Use "celsius" to "fahrenheit" or "fahrenheit" to "celsius"'
            }), 400
        
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/', methods=['GET'])
def index():
    """Home page with API information"""
    return jsonify({
        'name': 'Temperature Conversion API',
        'version': '1.0.0',
        'endpoints': {
            'health': {
                'method': 'GET',
                'path': '/health',
                'description': 'Check API status'
            },
            'celsius_to_fahrenheit': {
                'method': 'POST',
                'path': '/convert/celsius-to-fahrenheit',
                'description': 'Convert Celsius to Fahrenheit',
                'body': {'temperature': 'number'}
            },
            'fahrenheit_to_celsius': {
                'method': 'POST',
                'path': '/convert/fahrenheit-to-celsius',
                'description': 'Convert Fahrenheit to Celsius',
                'body': {'temperature': 'number'}
            },
            'convert': {
                'method': 'POST',
                'path': '/convert',
                'description': 'Generic conversion',
                'body': {
                    'temperature': 'number',
                    'from_unit': 'celsius|fahrenheit',
                    'to_unit': 'celsius|fahrenheit'
                }
            }
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
