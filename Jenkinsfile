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
                    if (isUnix()) {
                        sh 'docker build -f Dockerfile.app -t $DOCKER_IMAGE_API .'
                    } else {
                        bat 'docker build -f Dockerfile.app -t %DOCKER_IMAGE_API% .'
                    }
                }
            }
        }

        stage('Build Test Docker Image') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'docker build -f Dockerfile.test -t $DOCKER_IMAGE_TEST .'
                    } else {
                        bat 'docker build -f Dockerfile.test -t %DOCKER_IMAGE_TEST% .'
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Runs the tests in the test container
                    if (isUnix()) {
                        sh 'docker run --rm $DOCKER_IMAGE_TEST'
                    } else {
                        bat 'docker run --rm %DOCKER_IMAGE_TEST%'
                    }
                }
            }
        }

        stage('Clean Up') {
            steps {
                script {
                    // Remove stopped containers (optional)
                    if (isUnix()) {
                        sh 'docker container prune -f || true'
                    } else {
                        bat 'docker container prune -f'
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up old images (optional)
            script {
                if (isUnix()) {
                    sh 'docker image prune -f || true'
                } else {
                    bat 'docker image prune -f'
                }
            }
        }
        success {
            echo 'Build and tests completed successfully!'
        }
        failure {
            echo 'Build or tests failed.'
        }
    }
}
