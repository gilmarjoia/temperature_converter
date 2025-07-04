pipeline {
    agent any

    environment {
        DOCKER_IMAGE_API = 'temperature-converter-api'
        DOCKER_IMAGE_TEST = 'temperature-converter-test'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build API Docker Image') {
            steps {
                script {
                    sh 'docker build -f Dockerfile.app -t $DOCKER_IMAGE_API .'
                }
            }
        }

        stage('Build Test Docker Image') {
            steps {
                script {
                    sh 'docker build -f Dockerfile.test -t $DOCKER_IMAGE_TEST .'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Runs the tests in the test container
                    sh 'docker run --rm $DOCKER_IMAGE_TEST'
                }
            }
        }

        stage('Clean Up') {
            steps {
                script {
                    // Remove stopped containers (optional)
                    sh 'docker container prune -f || true'
                }
            }
        }
    }

    post {
        always {
            // Clean up old images (optional)
            sh 'docker image prune -f || true'
        }
        success {
            echo 'Build and tests completed successfully!'
        }
        failure {
            echo 'Build or tests failed.'
        }
    }
}
