
pipeline {
    agent any

    environment {
        IMAGE_NAME = "varsha072/qrgen"
        IMAGE_TAG = "latest"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Docker Image') {
            steps {
                bat '''
                    docker pull %IMAGE_NAME%:%IMAGE_TAG%
                    if errorlevel 1 exit /b 1
                '''
            }
        }

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

        stage('Verify Deployment') {
            steps {
                bat '''
                    kubectl get pods
                    kubectl get services
                '''
            }
        }
    }

    post {
        success {
            echo 'QRGen Kubernetes deployment completed successfully!'
        }

        failure {
            echo 'QRGen deployment failed. Check the console output.'
        }
    }
}
