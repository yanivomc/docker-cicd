job('SOA Manual - PipeLine') {
    steps {
        shell('SOA DSL CONFIGURED!')
    }
}

pipelineJob('github-demo') {
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