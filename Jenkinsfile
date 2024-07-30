pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Khalil-Bouazizi/Flask-Project.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python test.py'
            }
        }
    }
}
