node{
    stage('SonarQube Analysis'){
        def scannerHome = tool 'SonarQubeInstaller'
        withSonarQubeEnv('SonarQube'){
            sh """ls
                /var/lib/jenkins/tools/hudson.plugins.sonar.SonarRunnerInstallation/SonarQubeInstaller/bin/sonar-scanner
                ls /var/lib/jenkins/workspace/KryonFhir
                 """
        }
    }
}