job('NodeJS Docker example') {
    scm {
        git('https://github.com/yanivomc/docker-cicd.git','master') {  node -> // is hudson.plugins.git.GitSCM
            node / gitConfigName('DSL User')
            node / gitConfigEmail('jenkins-dsl@devophift.work')
        }
    }
    triggers {
        scm('H/5 * * * *')
    }
   
    
    steps {
        dockerBuildAndPublish {
            repositoryName('aviad539/amdocsapp')
            tag('${GIT_REVISION,length=9}')
            registryCredentials('769ab113-cc97-4c17-9c90-55e2b40b8031')
            buildContext('./basics/')
            forcePull(false)
            forceTag(false)
            createFingerprints(false)
            skipDecorate()
        }
    }
}

