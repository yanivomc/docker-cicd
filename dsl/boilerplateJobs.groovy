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
                        credentials(gitCredentialsId)
                    }
                    branches('jenkins_docker')
                    scriptPath('buildroot.pipeline')
                    extensions {
                        cloneOptions {
                            shallow(true)
                            depth(1)
                            timeout(30)
                        }
                    }
                }
            }
        }
    }
    triggers {
        scm('H/5 * * * *')
    }
}

pipelineJob('u-boot') {
    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url(gitUrlUboot)
                        credentials(gitCredentialsId)
                    }
                    branches('jenkins_docker')
                    scriptPath('u-boot.pipeline')
                    extensions {
                        cloneOptions {
                            shallow(true)
                            depth(1)
                            timeout(30)
                        }
                    }
                }
            }
        }
    }
    triggers {
        scm('H/5 * * * *')
    }
}

pipelineJob('kernel') {
    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url(gitUrlKernel)
                        credentials(gitCredentialsId)
                    }
                    branches('jenkins_docker')
                    scriptPath('kernel.pipeline')
                    extensions {
                        cloneOptions {
                            shallow(true)
                            depth(1)
                            timeout(30)
                        }
                    }
                }
            }
        }
    }
    triggers {
        scm('H/5 * * * *')
    }
}
