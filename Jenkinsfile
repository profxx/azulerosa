pipeline {
    agent any

    triggers {
        githubPush()
    }
    stages {
        stage('Build') {
            steps {
                sh "docker-compose up -d --build"                
            }

        }

    }
}