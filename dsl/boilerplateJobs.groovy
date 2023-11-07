// Define job internal variables
def gitUrl = 'http://gitlab.satixfy.lan/sw_host/buildroot.git'
def gitCredentialsId = 'git-credentials-id' // Replace with your actual Jenkins credentials ID
def pipelineScriptPath = 'buildroot.pipeline' // Path to your pipeline script within the repo

pipelineJob('buildroot') {
    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url(gitUrl)
                        credentials(gitCredentialsId) // Replace with your actual Jenkins credentials ID
                    }
                    branches('jenkins_docker')
                    scriptPath(pipelineScriptPath)
                }
            }
        }
    }
    triggers {
        scm('H/5 * * * *') // Triggers the build when a change is detected in the repository every 5 minutes
    }
}
