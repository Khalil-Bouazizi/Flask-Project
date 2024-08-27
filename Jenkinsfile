pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Khalil-Bouazizi/Flask-Project.git'
            }
        }

        stage('Build and Run Docker Containers') {
            steps {
                sh 'docker-compose up -d --build'
            }
        }

        stage('Test Docker Image with Trivy') {
            steps {
                sh 'trivy image khalilbouazizii/flask_app_devops'
            }
        }

        stage('Push Docker Image to DockerHub') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'docker_pwd', variable: 'DockerHubPwd')]) {
                        sh 'docker login -u khalilbouazizii -p $DockerHubPwd'
                    }
                    sh 'docker tag khalilbouazizii/flask_app_devops:latest khalilbouazizii/flask_app_devops:latest'
                    sh 'docker push khalilbouazizii/flask_app_devops:latest'
                }
            }
        }
    }
}
