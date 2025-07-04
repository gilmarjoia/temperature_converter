# Temperature Conversion API

A simple Flask API to convert temperatures between Celsius and Fahrenheit.

## Features

- Convert Celsius to Fahrenheit
- Convert Fahrenheit to Celsius
- Health check endpoint
- Input validation
- Error handling

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## Docker Usage

You can use Docker and Docker Compose to build and run the API and tests easily.

### Build and Run Both Services (API + Tests)

Using Docker Compose (recommended):

```bash
docker-compose up --build
```

This will start both the API service and the test service. The API will be available at [http://localhost:5000](http://localhost:5000).

### Run Only the API Service

```bash
docker-compose up --build api
```

### Run Only the Test Service

```bash
docker-compose up --build test
```

### Manual Docker Commands

If you prefer to use Docker directly:

**Build and Run the API:**
```bash
docker build -f Dockerfile.app -t temperature-converter-api .
docker run -d --name temperature-api -p 5000:5000 temperature-converter-api
```

**Run All Tests in a Container:**
```bash
docker build -f Dockerfile.test -t temperature-converter-test .
docker run --rm temperature-converter-test
```

### Using the Helper Script

You can also use the provided script for common tasks:

```bash
./docker-build.sh build-all   # Build both containers
./docker-build.sh start       # Build and start the API
./docker-build.sh test        # Build and run all tests
./docker-build.sh cleanup     # Stop and remove containers
```

**Note for Windows users:**
> Use `docker-build.bat` instead of `docker-build.sh` when running scripts manually on Windows.

## Endpoints

### 1. Health Check
**GET** `/health`

Checks if the API is working.

**Response:**
```json
{
  "status": "healthy",
  "message": "Temperature conversion API is working"
}
```

### 2. Convert Celsius to Fahrenheit
**POST** `/convert/celsius-to-fahrenheit`

**Body:**
```json
{
  "temperature": 25
}
```

**Response:**
```json
{
  "celsius": 25,
  "fahrenheit": 77.0,
  "message": "25°C = 77.0°F"
}
```

### 3. Convert Fahrenheit to Celsius
**POST** `/convert/fahrenheit-to-celsius`

**Body:**
```json
{
  "temperature": 77
}
```

**Response:**
```json
{
  "fahrenheit": 77,
  "celsius": 25.0,
  "message": "77°F = 25.0°C"
}
```

### 4. Generic Conversion
**POST** `/convert`

**Body:**
```json
{
  "temperature": 25,
  "from_unit": "celsius",
  "to_unit": "fahrenheit"
}
```

**Response:**
```json
{
  "temperature": 25,
  "from_unit": "celsius",
  "to_unit": "fahrenheit",
  "result": 77.0,
  "message": "25°C = 77.0°F"
}
```

### 5. API Information
**GET** `/`

Returns information about all available endpoints.

## Usage Examples

### Using curl

**Convert 25°C to Fahrenheit:**
```bash
curl -X POST http://localhost:5000/convert/celsius-to-fahrenheit \
  -H "Content-Type: application/json" \
  -d '{"temperature": 25}'
```

**Convert 77°F to Celsius:**
```bash
curl -X POST http://localhost:5000/convert/fahrenheit-to-celsius \
  -H "Content-Type: application/json" \
  -d '{"temperature": 77}'
```

### Using Python requests

```python
import requests

# Convert Celsius to Fahrenheit
response = requests.post('http://localhost:5000/convert/celsius-to-fahrenheit', 
                        json={'temperature': 25})
print(response.json())

# Convert Fahrenheit to Celsius
response = requests.post('http://localhost:5000/convert/fahrenheit-to-celsius', 
                        json={'temperature': 77})
print(response.json())
```

## HTTP Status Codes

- **200**: Success
- **400**: Validation error (invalid data)
- **500**: Internal server error

## Error Handling

The API returns clear error messages in English:

```json
{
  "error": "Invalid temperature value. Must be a number."
}
```

## Development

### Running Tests

**Local:**
```bash
python -m pytest tests/ -v
```

**With Docker:**
```bash
docker-compose up --build test
```

### Project Structure

```
temperature_converter/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile.app         # API container configuration
├── Dockerfile.test        # Test container configuration
├── docker-build.sh        # Build script (Linux/Mac)
├── docker-build.bat       # Build script (Windows)
├── Jenkinsfile           # CI/CD pipeline
├── src/
│   ├── __init__.py
│   └── temperature_converter.py  # Core conversion logic
└── tests/
    ├── __init__.py
    ├── test_app.py        # API endpoint tests
    └── test_temperature_converter.py  # Unit tests
```

## CI/CD

This project includes a Jenkins pipeline (`Jenkinsfile`) that:
- Builds Docker images for both API and test containers
- Runs all tests in a containerized environment
- Cleans up resources after completion

The pipeline is designed to work on both Linux and Windows Jenkins agents.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE). 