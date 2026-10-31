
pipeline {
    agent any

    environment {
        IMAGE_NAME = "varsha072/qrgen"
        IMAGE_TAG = "latest"

        // Use the Kubernetes configuration that works in CMD
        KUBECONFIG = 'C:/Users/akkip/.kube/config'
    }

    stages {

        // Stage 1: Checkout source code
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // Stage 2: Verify Docker image
        stage('Verify Docker Image') {
            steps {
                bat '''
                    docker pull %IMAGE_NAME%:%IMAGE_TAG%
                    if errorlevel 1 exit /b 1
                '''
            }
        }

        // Stage 3: Check Kubernetes configuration
        stage('Check Kubernetes Config') {
            steps {
                bat '''
                    whoami
                    echo USERPROFILE=%USERPROFILE%

                    kubectl config current-context
                    if errorlevel 1 exit /b 1

                    kubectl config view --minify -o jsonpath="{.clusters[0].cluster.server}"
                    echo.
                '''
            }
        }

        // Stage 4: Deploy application
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

        // Stage 5: Verify deployment
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
