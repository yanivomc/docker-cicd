pipelineJob('SOA Manual - PipeLine') {
    definition {
        cpsScm {
            scm {
                git {
                    branch('guardbox')
                    remote {
                        github('https://github.com/yanivomc/docker-cicd.git')
                    }
                }
            }
            scriptPath('declarative-examples/simple-examples/environmentInStage.groovy')
        }
    }
}