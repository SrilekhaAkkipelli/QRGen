
pipeline {
    agent any

    environment {
        IMAGE_NAME = "varsha072/qrgen"
        IMAGE_TAG = "latest"
    }

    stages {

        // Stage 1: Checkout source code from GitHub
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // Stage 2: Build Docker image
        stage('Build Docker Image') {
            steps {
                bat '''
                    docker build -t %IMAGE_NAME%:%IMAGE_TAG% .
                    if errorlevel 1 exit /b 1
                '''
            }
        }

        // Stage 3: Push Docker image to Docker Hub
        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'qrgen-dockerhub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    bat '''
                        echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                        if errorlevel 1 exit /b 1

                        docker push %IMAGE_NAME%:%IMAGE_TAG%
                        if errorlevel 1 exit /b 1

                        docker logout
                    '''
                }
            }
        }

        // Stage 4: Deploy application to Kubernetes
        stage('Deploy to Kubernetes') {
            steps {
                bat '''
                    kubectl apply -f kubernetes/deployment.yaml
                    if errorlevel 1 exit /b 1

                    kubectl apply -f kubernetes/service.yaml
                    if errorlevel 1 exit /b 1

                    kubectl rollout status deployment/qrgen-deployment
                    if errorlevel 1 exit /b 1
                '''
            }
        }
    }

    // Post-build actions
    post {
        success {
            echo 'QRGen CI/CD Pipeline completed successfully!'
        }

        failure {
            echo 'QRGen CI/CD Pipeline failed. Check the console output.'
        }
    }
}
