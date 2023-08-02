pipeline {
    agent any
    stages {
        stage('Sonar Analytics') {
            steps {
                script {
                def scannerHome = tool  'SonarQube'
                    withSonarQubeEnv('SonarQube') {
                    sh "ls"
                    sh "ls ${scannerHome}"
                    }
                }
            }
        }
    }
}