pipeline {
    agent any

    stages {
        stage('BUILD - Install tools for Python3 Virtual Environment') {
            steps {
                sh 'jenkins/01-install-tools.sh'
            }
        }

        stage('BUILD - Create Python3 Virtual Environment') {
            steps {
                sh 'jenkins/02-create-environment.sh'
            }
        }

        stage('BUILD - Install dependencies') {
            steps {
                sh 'jenkins/03-install-dependencies.sh'
            }
        }

        stage('TEST - Unit testing') {
            steps {
                sh 'jenkins/04-testing.sh'
            }
        }
    }
}

