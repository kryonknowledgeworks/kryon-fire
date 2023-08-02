pipeline {
    agent any
    stages {
        stage('Sonar Analytics') {
            steps {
            def scannerHome = tool  'SonarQube'
                script {
                    withSonarQubeEnv('SonarQube') {
                    sh "ls"
                    sh "ls ${scannerHome}"
                    }
                }
            }
        }
    }
}