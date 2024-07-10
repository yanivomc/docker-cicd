job('NodeJS Docker example') {
    scm {
        git('git://github.com/Guy-Zamir-78/docker-cicd.git','master') {  node -> // is hudson.plugins.git.GitSCM
            node / gitConfigName('DSL User')
            node / gitConfigEmail('jenkins-dsl@devophift.work')
        }
    }
    triggers {
        scm('H/5 * * * *')
    }
   
    
    steps {
        dockerBuildAndPublish {
            repositoryName('Guy-Zamir-78/amdocsapp')
            tag('${GIT_REVISION,length=9}')
            registryCredentials('guydocker')
            buildContext('./basics/')
            forcePull(false)
            forceTag(false)
            createFingerprints(false)
            skipDecorate()
        }
    }
}

