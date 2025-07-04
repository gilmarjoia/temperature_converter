#!/bin/bash

# Temperature Converter API Docker Build Script

echo "🌡️  Temperature Converter API - Docker Build Script"
echo "=================================================="

# Function to build API container
build_api() {
    echo "🔨 Building API container..."
    docker build -f Dockerfile.app -t temperature-converter-api .
    if [ $? -eq 0 ]; then
        echo "✅ API container built successfully!"
    else
        echo "❌ Failed to build API container"
        exit 1
    fi
}

# Function to build test container
build_test() {
    echo "🧪 Building test container..."
    docker build -f Dockerfile.test -t temperature-converter-test .
    if [ $? -eq 0 ]; then
        echo "✅ Test container built successfully!"
    else
        echo "❌ Failed to build test container"
        exit 1
    fi
}

# Function to run API container
run_api() {
    echo "🚀 Starting API container..."
    docker run -d --name temperature-api -p 5000:5000 temperature-converter-api
    if [ $? -eq 0 ]; then
        echo "✅ API container started successfully!"
        echo "🌐 API available at: http://localhost:5000"
        echo "📊 Health check: http://localhost:5000/health"
    else
        echo "❌ Failed to start API container"
        exit 1
    fi
}

# Function to run tests
run_tests() {
    echo "🧪 Running tests..."
    docker run --rm temperature-converter-test
    if [ $? -eq 0 ]; then
        echo "✅ All tests passed!"
    else
        echo "❌ Some tests failed"
        exit 1
    fi
}

# Function to stop and clean containers
cleanup() {
    echo "🧹 Cleaning up containers..."
    docker stop temperature-api 2>/dev/null || true
    docker rm temperature-api 2>/dev/null || true
    echo "✅ Cleanup completed!"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  build-api    Build the API container"
    echo "  build-test   Build the test container"
    echo "  build-all    Build both containers"
    echo "  run-api      Run the API container"
    echo "  run-tests    Run the test container"
    echo "  test         Build and run tests"
    echo "  start        Build and start API"
    echo "  stop         Stop API container"
    echo "  cleanup      Stop and remove containers"
    echo "  help         Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 build-all    # Build both containers"
    echo "  $0 start        # Build and start API"
    echo "  $0 test         # Build and run tests"
}

# Main script logic
case "$1" in
    "build-api")
        build_api
        ;;
    "build-test")
        build_test
        ;;
    "build-all")
        build_api
        build_test
        ;;
    "run-api")
        run_api
        ;;
    "run-tests")
        run_tests
        ;;
    "test")
        build_test
        run_tests
        ;;
    "start")
        build_api
        run_api
        ;;
    "stop")
        docker stop temperature-api 2>/dev/null || echo "No API container running"
        ;;
    "cleanup")
        cleanup
        ;;
    "help"|"--help"|"-h"|"")
        show_usage
        ;;
    *)
        echo "❌ Unknown option: $1"
        show_usage
        exit 1
        ;;
esac 