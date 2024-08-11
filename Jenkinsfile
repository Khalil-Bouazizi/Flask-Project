pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Khalil-Bouazizi/Flask-Project.git'
            }
        }

        stage('SonarQube analysis') {
            steps {
                script {
                    def scannerHome = tool name: 'sonarqube', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                    withSonarQubeEnv('sonarqube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.login=admin \
                            -Dsonar.password=khalil \
                            -Dsonar.projectKey=devops_CI \
                            -Dsonar.exclusions=vendor/**,resources/**,**/*.java \
                            -Dsonar.host.url=http://20.84.116.93:9000/
                        """
                    }
                }
            }
        }

        stage('Build and Run Docker Containers') {
            steps {
                sh 'docker-compose up -d'
            }
        }

        stage('Test Docker Image with Trivy') {
            steps {
                sh 'trivy image khalilbouazizii/flask_app_devops > resumetest.txt'
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
