pipeline {
    agent any
    stages {
        stage('Sonar Analytics') {
            steps {
                script {

                    withSonarQubeEnv('SonarQube') {
                    sh "ls"
                    sh "/opt/sonar-scanner/bin/sonar-scanner"
                    sh "sonar-scanner -Dsonar.projectKey=KryonFhir -Dsonar.sources=core -Dsonar.host.url=https://sonar.kkwtk.com -Dsonar.login=sqp_649f7d8b01e0afc70d77846e9d8180b7f3585f8b"
                    }
                }
            }
        }
    }
}