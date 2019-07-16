node('docker-slave-0d1cf2ec3e3f') {

    stage 'Checkout'
        checkout scm
    stage 'Build & UnitTest'
    sh "docker build -t account_app:B${BUILD_NUMBER} -f Dockerfile ."
    sh "docker build -t account_app:test-B${BUILD_NUMBER} -f Dockerfile.Integration ."
    
    // stage 'Pusblish UT Reports'
        
    //     containerID = sh (
    //         script: "docker run -d account_app:B${BUILD_NUMBER}", 
    //     returnStdout: true
    //     ).trim()
    //     echo "Container ID is ==> ${containerID}"
    //     sh "docker cp ${containerID}:/TestResults/test_results.xml test_results.xml"
    //     sh "docker stop ${containerID}"
    //     sh "docker rm ${containerID}"
    //     step([$class: 'MSTestPublisher', failOnError: false, testResultsFile: 'test_results.xml'])    
      
    stage 'Integration Test'
        //sh 'docker-compose -f docker-compose.integration.yml up'
        sh "docker-compose -f docker-compose.integration.yml up --force-recreate --abort-on-container-exit"
        sh "docker-compose -f docker-compose.integration.yml down -v"
}
