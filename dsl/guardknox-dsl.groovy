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
                    remote {
                        github('jenkinsci/pipeline-examples')
                    }
                }
            }
            scriptPath('declarative-examples/simple-examples/environmentInStage.groovy')
        }
    }
}