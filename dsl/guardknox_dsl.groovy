pipelineJob('SOA Manual - PipeLine') {
    definition {
        cpsScm {
            scm {
                git {
                    branch('guardbox')
                    remote {
                        github('yanivomc/docker-cicd')
                    }
                }
            }
            scriptPath('./Jenkinsfile')
        }
    }
}