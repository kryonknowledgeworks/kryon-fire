pipeline {
  agent any
  stages {
    stage('SonarQube Analysis') {
      def scannerHome = tool 'SonarQube'
      withSonarQubeEnv('SonarQube') {
        sh ""
        "/var/lib/jenkins/tools/hudson.plugins.sonar.SonarRunnerInstallation/SonarQube/bin/sonar-scanner \
        -D sonar.projectVersion=1.0-SNAPSHOT \
        -D sonar.login=admin \
        -D sonar.password=Shift123#@! \
        -D sonar.projectBaseDir=/var/lib/jenkins/workspace/jenkins-sonar/ \
        -D sonar.projectKey=fhir \
        -D sonar.sourceEncoding=UTF-8 \
        -D sonar.language=py \
        -D sonar.sources=core -
        -D sonar.host.url = https: //sonar.kkwtk.com/"""
      }
    }
  }
}