pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Khalil-Bouazizi/Flask-Project.git'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python test.py'
            }
        }
    }
}
