job('buildroot') {
    // Define job internal variables
    def gitUrl = 'http://gitlab.satixfy.lan/sw_host/buildroot.git'
    def gitCredentialsId = 'git-credentials-id' // Replace with your actual Jenkins credentials ID
    def dockerRepo = 'satixfy' // Replace with your actual Docker Repo name
    def dockerImageName = "${dockerRepo}/u-boot" // Replace with your actual Docker image name
    def dockerImageTag = "\${env.BUILD_NUMBER}" // use jenkins build number as tag
    
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
        shell("docker build -t ${dockerImageName}:${dockerImageTag} -f buildroot.Dockerfile .")
        // shell('docker push satixfy/u-boot') // Ignored for now.
    }
}
