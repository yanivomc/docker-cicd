// Define job internal variables
def gitUrlBuildroot = 'http://gitlab.satixfy.lan/sw_host/buildroot.git'
def gitUrlUboot = 'http://gitlab.satixfy.lan/sw_host/u-boot.git'
def gitUrlKernel = 'http://gitlab.satixfy.lan/sw_host/linux.git'
def gitCredentialsId = 'git-credentials-id' // Replace with your actual Jenkins credentials ID


pipelineJob('buildroot') {
    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url(gitUrlBuildroot)
                        credentials(gitCredentialsId) // Replace with your actual Jenkins credentials ID
                    }
                    branches('jenkins_docker')
                    scriptPath('buildroot.pipeline')
                }
            }
        }
    }
    triggers {
        scm('H/5 * * * *') // Triggers the build when a change is detected in the repository every 5 minutes
    }
}

pipelineJob('u-boot') {
    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url(gitUrlUboot)
                        credentials(gitCredentialsId) // Replace with your actual Jenkins credentials ID
                    }
                    branches('jenkins_docker')
                    scriptPath('/buildroot/u-boot.pipeline')
                }
            }
        }
    }
    triggers {
        scm('H/5 * * * *') // Triggers the build when a change is detected in the repository every 5 minutes
    }
}


pipelineJob('kernel') {
    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url(gitUrlKernel)
                        credentials(gitCredentialsId) // Replace with your actual Jenkins credentials ID
                    }
                    branches('jenkins_docker')
                    scriptPath('/buildroot/kernel.pipeline')
                }
            }
        }
    }
    triggers {
        scm('H/5 * * * *') // Triggers the build when a change is detected in the repository every 5 minutes
    }
}