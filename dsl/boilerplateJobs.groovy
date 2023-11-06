job('buildroot') {
    // Define job internal variables
    def gitUrl = 'http://gitlab.satixfy.lan/sw_host/buildroot.git'
    def gitCredentialsId = 'git-credentials-id' // Replace with your actual Jenkins credentials ID
    def registryCreds = 'satixfyrepo' // Replace with your actual Jenkins credentials ID
    def dockerRepo = ' satixfy-repo.devopshift.com' // Replace with your actual Docker Repo name
    def dockerImageName = "${dockerRepo}/buildroot/buildroot" // Replace with your actual Docker image name
    def dockerImageTag = "\${BUILD_NUMBER}" // use jenkins build number as tag
    def dockerFile = 'buildroot.Dockerfile'
    
    scm {
        git {
            remote {
                url(gitUrl)
                credentials(gitCredentialsId) // Replace with your actual Jenkins credentials ID
            }
            branch('jenkins_docker')
        }
    }
    triggers {
        scm('H/5 * * * *') // Triggers the build when a change is detected in the repository every 5 minutes
    }

    steps {
        // Your Docker build and push plugin code here


        dockerBuildAndPush {
            repo(dockerImageName)
            tag(dockerImageTag)
            registryCredentialsId(registryCreds)
            dockerfilePath(dockerFile)
            forcePull(false)
        }
    }
}
```
job('kernel') {
    // Define job internal variables
    def gitUrl = 'http://gitlab.satixfy.lan/sw_host/kernel.git'
    def gitCredentialsId = 'git-credentials-id' // Replace with your actual Jenkins credentials ID
    def registryCreds = 'satixfyrepo' // Replace with your actual Jenkins credentials ID
    def dockerRepo = 'satixfyrepo' // Replace with your actual Docker Repo name
    def dockerImageName = "${dockerRepo}/kernel" // Replace with your actual Docker image name
    def dockerImageTag = "\${BUILD_NUMBER}" // use jenkins build number as tag
    def dockerFile = 'kernel.Dockerfile'
    
    scm {
        git {
            remote {
                url(gitUrl)
                credentials(gitCredentialsId) // Replace with your actual Jenkins credentials ID
            }
            branch('jenkins_docker')
        }
    }
    triggers {
        scm('H/5 * * * *') // Triggers the build when a change is detected in the repository every 5 minutes
    }

    steps {
         dockerBuildAndPush {
            repo(dockerImageName)
            tag(dockerImageTag)
            registryCredentialsId(registryCreds)
            dockerfilePath(dockerFile)
            forcePull(false)
        }
    }
}
