//Manual pipeline
pipeline {
    agent { label ('docker') }
    environment {
        BuildResult = "Build - did not run \n"
        UnitTestResult = "Unit Test - did not run \n"
        DocWarnings = "Doxygen Warnings - did not run \n"
        DocResult = "Doxygen - was not uploaded \n"
        PackageResults = "Unified Package - was not uploaded \n"
        ArtifactoryResults = "Package - did not run \n"
    }
    stages {
        stage ('Environment Variables and Functions') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'GITLAB', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    script {
                        FAILED_STAGE = functions.stagefailed()
                        loadEnvVar()
                        paramSelect()
                        ChoicesStaticMap = [ All:'false',Build:'false',Install:'false',Test:'false',Package:'false',Doxygen:'false']
                        ChoicesMap = functions.listToMap(params['Choices'].split(','),ChoicesStaticMap)
                    }
                }
            }
        }
        // Clean Previous Build
        stage ('Clean') {
            steps {
                script {FAILED_STAGE = functions.stagefailed()}
                cleanWs()
            }
        }
        // Pull SOA Code
        stage ('Pull') {
            steps {
                script {FAILED_STAGE = functions.stagefailed()}
                // checkout for soa project
                checkout([$class: 'GitSCM', branches: [[name: '$Branch']], extensions: [], userRemoteConfigs: [[credentialsId: 'GITLAB', url: "${PROJECTREPO}"]]])
                // checkout for python scripts for generating reports
                checkout([$class: 'GitSCM', branches: [[name: "${GIT_BRANCH}"]], extensions: [[$class: 'SparseCheckoutPaths', sparseCheckoutPaths: [[path: 'scripts']]], [$class: 'RelativeTargetDirectory', relativeTargetDir: "${DEVOPSDIR}"]], userRemoteConfigs: [[credentialsId: 'GITLAB', url: "${DEVOPSREPO}"]]])
                sh '''#!/bin/bash
                cd "build"
                chmod +x -R soa_python
                '''
            }
        }
        stage ('Parallel') {
            failFast true
            parallel {
                // Build for X86-64 Selection
                stage ('x86-64') {
                    environment {
                    SDK="${X86SDK}"
                    Architecture="x86_64"
                    }
                    agent { label ('docker') }
                    when {
                        anyOf {
                            environment name: 'Choose_SDK', value: 'x86-64'
                            environment name: 'Choose_SDK', value: 'All'
                        }
                    }
                    stages {
                        // Clean Previous Build
                        stage ('Clean_X86-64') {
                            steps {
                                script{FAILED_STAGE = functions.stagefailed()}
                                cleanWs()
                            }
                        }
                        stage ('Pull_X86-64') {
                            steps {
                                script {FAILED_STAGE = functions.stagefailed()}
                                // checkout for soa project
                                checkout([$class: 'GitSCM', branches: [[name: '$Branch']], extensions: [], userRemoteConfigs: [[credentialsId: 'GITLAB', url: "${PROJECTREPO}"]]])
                                // checkout for python scripts for generating reports
                                checkout([$class: 'GitSCM', branches: [[name: "${GIT_BRANCH}"]], extensions: [[$class: 'SparseCheckoutPaths', sparseCheckoutPaths: [[path: 'scripts']]], [$class: 'RelativeTargetDirectory', relativeTargetDir: "${DEVOPSDIR}"]], userRemoteConfigs: [[credentialsId: 'GITLAB', url: "${DEVOPSREPO}"]]])
                                sh '''#!/bin/bash
                                cd "build"
                                chmod +x -R soa_python
                                '''
                            }
                        }
                        stage ('Build_x86-64') {
                            when { expression { ChoicesMap['Build'] == 'true' } }
                            steps {
                                script {FAILED_STAGE = functions.stagefailed()}
                                // Build using x86-64 build script
                                sh '''#!/bin/bash
                                cd build
                                soa_python/scripts/build.sh
                                '''
                                script {
                                    //FAILED_STAGE = functions.stagefailed()
                                    env.errorx86 = sh returnStdout:true, script:
                                    '''
                                    cd "build/soa_python/scripts"
                                    python3 builderr.py
                                    '''
                                    env.warnx86 = sh returnStdout:true, script:
                                    '''
                                    cd "build/soa_python/scripts"
                                    python3 buildwar.py
                                    '''
                                    if (env.errorx86.trim() == '0' ) {
                                    echo "${env.errorx86}"
                                    }
                                    else {
                                    sh "exit 1"
                                    }
                                }
                            }
                        }
                        // Install using install build script
                        stage ('install_X86-64') {
                            when { expression { ChoicesMap['Install'] == 'true' } }
                            steps {
                                script {FAILED_STAGE = functions.stagefailed()}
                                sh '''#!/bin/bash
                                build/soa_python/scripts/install.sh
                                '''
                            }
                        }
                        // run unit test 
                        stage ('test_X86-64') {
                            when { expression { ChoicesMap['Test'] == 'true' } }
                            options {
                                timeout(time: 10, unit: 'MINUTES')
                            }
                            steps {
                                sh '''#!/bin/bash
                                build/soa_python/scripts/qemu.sh
                                '''
                            }
                            post {
                                failure {
                                script {FAILED_STAGE = functions.stagefailed()}
                                    sh '''#!/bin/bash
                                    build/soa_python/scripts/packagebuild.sh
                                    '''
                                }
                            }
                        }
                        // upload HTML Report to apache
                        stage ('upload report x86') {
                            when { expression { ChoicesMap['Test'] == 'true' } }
                            steps {
                                    script {FAILED_STAGE = functions.stagefailed()}
                                    sh'''
                                    build/soa_python/scripts/copyreportapache.sh
                                    '''
                            }
                        } 
                        // package artifacts
                        stage ('package_X86-64') {
                            when { expression { ChoicesMap['Package'] == 'true' } }
                            steps {
                                script {FAILED_STAGE = functions.stagefailed()}
                                sh '''#!/bin/bash
                                build/soa_python/scripts/package.sh
                                '''
                            }
                        }
                        // copy artifact to packager
                        stage ('upload to artifactory x86-64') {
                            when { expression { ChoicesMap['Package'] == 'true' } }
                            steps {
                                script {FAILED_STAGE = functions.stagefailed()}
                                sh '''#!/bin/bash
                                build/soa_python/scripts/uploadartifactoryslave.sh
                                '''
                            }
                        }
                    }
                }
                // Build for AArch64 Selection
                stage ('AArch64') {
                    environment {
                    SDK="${AArch64SDK}"
                    Architecture="aarch64"
                    }
                    agent { label ('docker') }
                    when {
                        anyOf {
                            environment name: 'Choose_SDK', value: 'AArch64'
                            environment name: 'Choose_SDK', value: 'All'
                        }
                    }
                    stages {
                        // Clean Previous Build
                        stage ('Clean_AArch64') {
                            steps {
                                script {FAILED_STAGE = functions.stagefailed()}
                                cleanWs()
                            }
                        }
                        stage ('Pull_AArch64') {
                            steps {
                                script {FAILED_STAGE = functions.stagefailed()}
                                // checkout for soa project
                                checkout([$class: 'GitSCM', branches: [[name: '$Branch']], extensions: [], userRemoteConfigs: [[credentialsId: 'GITLAB', url: "${PROJECTREPO}"]]])
                                // checkout for python scripts for generating reports
                                checkout([$class: 'GitSCM', branches: [[name: "${GIT_BRANCH}"]], extensions: [[$class: 'SparseCheckoutPaths', sparseCheckoutPaths: [[path: 'scripts']]], [$class: 'RelativeTargetDirectory', relativeTargetDir: "${DEVOPSDIR}"]], userRemoteConfigs: [[credentialsId: 'GITLAB', url: "${DEVOPSREPO}"]]])
                                sh '''#!/bin/bash
                                cd "build"
                                chmod +x -R soa_python
                                '''
                            }
                        }
                        // Build using AArch64 build script
                        stage ('Build_AArch64') {
                            when { expression { ChoicesMap['Build'] == 'true' } }
                            steps {
                                script {FAILED_STAGE = functions.stagefailed()}
                                sh '''#!/bin/bash
                                cd build
                                soa_python/scripts/build.sh
                                '''
                                script {
                                    //FAILED_STAGE = functions.stagefailed()
                                    env.errorAArch64 = sh returnStdout:true, script:
                                    '''
                                    cd "build/soa_python/scripts"
                                    python3 builderr.py
                                    '''
                                    env.warnAArch64 = sh returnStdout:true, script:
                                    '''
                                    cd "build/soa_python/scripts"
                                    python3 buildwar.py
                                    '''
                                    if (env.errorAArch64.trim() == '0' ) {
                                    echo "${env.errorAArch64}"
                                    }
                                    else {
                                    sh "exit 1"
                                    }
                                }
                            }
                        }
                        // Install using install build script
                        stage ('install_AArch64') {
                            when { expression { ChoicesMap['Install'] == 'true' } }
                            steps {
                                script {FAILED_STAGE = functions.stagefailed()}
                                sh '''#!/bin/bash
                                build/soa_python/scripts/install.sh
                                '''
                            }
                        }
                        // run unit test
                        stage ('test_AArch64') {
                            when { expression { ChoicesMap['Test'] == 'true' } }
                            options {
                                timeout(time: 10, unit: 'MINUTES')
                            }
                            steps {
                                sh '''#!/bin/bash
                                build/soa_python/scripts/qemu.sh
                                '''
                            }
                            post {
                                failure {
                                script {FAILED_STAGE = functions.stagefailed()}
                                    sh '''#!/bin/bash
                                    build/soa_python/scripts/packagebuild.sh
                                    '''
                                }
                            }
                        }
                        // upload HTML Report to apache
                        stage ('upload report AArch64') {
                            when { expression { ChoicesMap['Test'] == 'true' } }
                            steps {
                                script {FAILED_STAGE = functions.stagefailed()}
                                withCredentials([usernameColonPassword(credentialsId: 'GITLAB', variable: 'USERPASS')]) {
                                sh'''
                                build/soa_python/scripts/copyreportapache.sh
                                '''
                                }
                            }
                        }
                        // package artifacts
                        stage ('package_AArch64') {
                            when { expression { ChoicesMap['Package'] == 'true' } }
                            steps {
                                script {FAILED_STAGE = functions.stagefailed()}
                                sh '''#!/bin/bash
                                build/soa_python/scripts/package.sh
                                '''
                            }
                        }
                        // copy artifact to packager
                        stage ('upload to artifactory AArch64') {
                            when { expression { ChoicesMap['Package'] == 'true' } }
                            steps {
                                script {FAILED_STAGE = functions.stagefailed()}
                                sh '''#!/bin/bash
                                build/soa_python/scripts/uploadartifactoryslave.sh
                                '''
                            }
                        }
                    }
                }
            }
        }
        // generate doxygen output into a file and copy in Branch_Time stracture
        stage ('doc') {
            when { expression { ChoicesMap['Doxygen'] == 'true' } }
            steps {
                script {FAILED_STAGE = functions.stagefailed()}
                withCredentials([usernameColonPassword(credentialsId: 'GITLAB', variable: 'USERPASS')]) {
                sh '''#!/bin/bash
                cd build
                soa_python/scripts/doc.sh
                '''
                }
                script {
                    env.docwarn = sh returnStdout:true, script:
                    '''
                    cd "build/soa_python/scripts"
                    python3 doc.py
                    '''
                }
            }
        }
        // copy doxygen to apache server
        stage ('copy to apache server') {
            when { expression { ChoicesMap['Doxygen'] == 'true' } }
            steps {
                sh '''#!/bin/bash
                build/soa_python/scripts/copydocapache.sh
                '''
                script {
                    FAILED_STAGE = functions.stagefailed()
                    DocWarnings = "Doxygen Warnings - ${env.docwarn}"
                    DocResult = "Doxygen Results - ${env.DOC} \n"
                }
            }
        }
        // download artifact with filtered name to a location on packager slave
        stage ('artifacts unify and clean') {
            when { expression { ChoicesMap['Package'] == 'true' } }
            steps {
                script {FAILED_STAGE = functions.stagefailed()}
                sh '''#!/bin/bash
                build/soa_python/scripts/downloadartifacts.sh
                '''
        // package all given artifact into a single artifact
                sh '''#!/bin/bash
                build/soa_python/scripts/unifyartifacts.sh
                '''
        // upload unified artifact to artifactory
                sh '''#!/bin/bash
                build/soa_python/scripts/uploadunified.sh
                '''
        // delete temporary artifacts (from build slaves) from local slave and from artifactory
                sh '''#!/bin/bash
                build/soa_python/scripts/deleteartifacts.sh
                '''
                script {
                    PackageResults = "You can download the artifact here - ${env.PackageURL} \n"
                    ArtifactoryResults = "Browse the artifact repository here - ${env.ArtifactoryURL}"
                }
            }
        }
    }
    post {
        success {
            script {
                // generate mail in case of success
                if (Choose_SDK == 'x86-64') {
                    if (ChoicesMap['Build'] == 'true') {
                    BuildResult = "Build Errors ${Choose_SDK} - ${env.errorx86}Warnings ${Choose_SDK} - ${env.warnx86}"
                    }
                    if (ChoicesMap['Test'] == 'true') {
                    UnitTestResult = "Unit Test Results ${Choose_SDK} - ${env.x86TEST} \n"
                    }
                }
                if (Choose_SDK == 'AArch64') {
                    if (ChoicesMap['Build'] == 'true') {
                    BuildResult = "Build Errors ${Choose_SDK} - ${env.errorAArch64}Warnings ${Choose_SDK} - ${env.warnAArch64}"
                    }
                    if (ChoicesMap['Test'] == 'true') {
                    UnitTestResult = "Unit Test Results ${Choose_SDK} - ${env.AArch64TEST} \n"
                    }
                }
                if (Choose_SDK == 'All') {
                    if (ChoicesMap['Build'] == 'true') {
                    BuildResult = "Build Errors x86-64 - ${env.errorx86}Warnings x86-64 - ${env.warnx86}"
                    BuildResult += "Build Errors AArch64 - ${env.errorAArch64}Warnings AArch64 - ${env.warnAArch64}"
                    }
                    if (ChoicesMap['Test'] == 'true') {
                    UnitTestResult = "Unit Test Results x86-64 - ${env.x86TEST} \n"
                    UnitTestResult += "Unit Test Results AArch64 - ${env.AArch64TEST} \n"
                    }
                }
                    emailext body: "$JOB_BASE_NAME Build # $BUILD_NUMBER Branch - ${Branch} \n" +
                                "Check console output at $BUILD_URL \n" +
                                "${UnitTestResult}" +
                                "${BuildResult}" +
                                "${DocResult}" +
                                "${DocWarnings}" +
                                "${PackageResults}" +
                                "${ArtifactoryResults}",
                                recipientProviders: [requestor()],
                                subject: '$JOB_BASE_NAME - Build # $BUILD_NUMBER - $BUILD_STATUS!'
            }
        }
        failure {
            script {
                if ("${FAILED_STAGE}" == 'test_X86-64' || "${FAILED_STAGE}" == 'test_AArch64' ) {
                    sh '''
                    build/soa_python/scripts/unifyandcleanbuild.sh
                    '''
                    BuildArtifact = "Workspace build artifact - ${BuildArtifactURL} \n"
                }
                else {
                    BuildArtifact = ""
                }
                // generate mail in case of failure
                    emailext body: "$JOB_BASE_NAME Build # $BUILD_NUMBER Branch - ${Branch} \n" +
                                "Check console output at $BUILD_URL \n" +
                                "Failed Stage - ${FAILED_STAGE} \n" +
                                "${BuildArtifact}",
                                recipientProviders: [requestor()],
                                subject: '$JOB_BASE_NAME - Build # $BUILD_NUMBER - $BUILD_STATUS!'
            }
        }
    }
}
