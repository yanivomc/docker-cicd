job('u-boot') {
    scm {
        git {
            remote {
                url('ssh://git@devop.satixfy.lan:222/sw_host/u-boot.git')
                credentials('git-credentials-id') // Replace with your actual Jenkins credentials ID
            }
            branch('linux/u-boot/u-boot')
        }
    }
    triggers {
    pollSCM('') // Triggers the build when a change is detected in the repository
    }

    steps {
        shell('docker build -t satixfy/u-boot .') // Replace with your actual Docker image name
        shell('docker push satixfy/u-boot') // Replace with your actual Docker image name
    }
}
