pipeline {
    agent any
    stages{
        stage('SonarQube') {
            steps {
            def scannerHome = tool 'sonar';
        withSonarQubeEnv(){

        sh "ls {scannerHome}"
        sh "${scannerHome}/bin/sonar-scanner --version"
        sh "sonar-scanner -Dsonar.projectKey=KryonFhir -Dsonar.sources=/core -Dsonar.host.url=https://sonar.kkwtk.com -Dsonar.login=sqp_649f7d8b01e0afc70d77846e9d8180b7f3585f8b"
        }
     }
 }
}
}