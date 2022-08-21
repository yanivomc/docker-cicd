docker-compose -f docker-compose-jenkins.yml build
(on every change of slave or master conf run the build command)

docker-compose -f docker-compose-jenkins.yml up -d


THE Job's def is located on folder ./dsl



you need to configure a freestyle job as followed:
Disable "Enable script security for Job DSL scripts" 
job name: boilerplate-soa
type: freestyle
repo: https://github.com/yanivomc/docker-cicd/
branch: */guardbox
build steps: Process Job DSLs
>>> Look on Filesystem
DSL SCRIPT: ./dsl/guardknox_dsl.groovy



