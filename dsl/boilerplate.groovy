job('Test example') { // Job NAME
    scm { // Configure Source control management 
        git('git://github.com/yanivomc/docker-demo.git') {  node -> // is hudson.plugins.git.GitSCM
            node / gitConfigName('DSL User')
            node / gitConfigEmail('jenkins-dsl@domain.com')
        }
    }
    triggers { // Configure when to check for changes 
        scm('H/5 * * * *')
    }
    
    steps { // what steps to take 
        shell("npm install")
    }
}
