@echo off
REM Temperature Converter API - Docker Build Script (Windows)

ECHO 🌡️  Temperature Converter API - Docker Build Script
ECHO ==================================================

REM Build API container
ECHO 🔨 Building API container...
docker build -f Dockerfile.app -t temperature-converter-api .
IF %ERRORLEVEL% EQU 0 (
    ECHO ✅ API container built successfully!
) ELSE (
    ECHO ❌ Failed to build API container
    EXIT /B 1
)

REM Build test container
ECHO 🧪 Building test container...
docker build -f Dockerfile.test -t temperature-converter-test .
IF %ERRORLEVEL% EQU 0 (
    ECHO ✅ Test container built successfully!
) ELSE (
    ECHO ❌ Failed to build test container
    EXIT /B 1
) 