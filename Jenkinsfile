pipeline {
    agent any
    stages {
        stage('Sonar Analytics') {
            steps {
                script {
                    withSonarQubeEnv('SonarQube') {
                    sh "ls"
                    }
                }
            }
        }
    }
}