pipeline {
    agent any
    stages {
        stage('Sonar Analytics') {
            steps {
                script {
                def scannerHome = tool 'SonarQubeScanner3'
                    withSonarQubeEnv('SonarQube') {
                    sh "ls"
                    sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }
    }
}