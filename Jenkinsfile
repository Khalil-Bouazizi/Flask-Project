pipeline {
    agent any

    stages {
        stage('Version') {
            steps {
                sh 'python3 --version'
            }
        }
        stage('Build') {
            steps {
                git url: 'https://github.com/Khalil-Bouazizi/Flask-Project.git'
            }
        }
        stage('Test') {
            steps {
                sh 'python test.py'
            }
        }
    }
}
