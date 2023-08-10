node{
 stage('Clone sources') {
        dir("Project") {
                    git(
                        url: "https://github.com/kryonknowledgeworks/kryon-fire.git",
                        branch: "sonar-path-file-issue",
                        changelog: true,
                        poll: true
                    )
                }
    }
    stage('SonarQube Analysis'){
        def scannerHome = tool 'SonarQubeInstaller'
        withSonarQubeEnv('SonarQube'){
            sh """ls
                /var/lib/jenkins/tools/hudson.plugins.sonar.SonarRunnerInstallation/SonarQubeInstaller/bin/sonar-scanner
                 """
        }
    }
}