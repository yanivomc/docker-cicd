# Starting off with the Jenkins base Image
FROM jenkins/jenkins:latest
 
# Installing the plugins we need using the in-built install-plugins.sh script instead of manual install plugins
RUN /usr/local/bin/install-plugins.sh git matrix-auth workflow-aggregator docker-workflow blueocean credentials-binding docker-build-publish job-dsl
 
# Setting up environment variables for Jenkins admin user
ENV JENKINS_USER admin
ENV JENKINS_PASS admin
 
# Skip the initial setup wizard
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false -Dhudson.security.csrf.DefaultCrumbIssuer.EXCLUDE_SESSION_ID=true
 
# Start-up scripts to set number of executors and creating the admin user
COPY executors.groovy /usr/share/jenkins/ref/init.groovy.d/
COPY default-user.groovy /usr/share/jenkins/ref/init.groovy.d/
 
VOLUME /var/jenkins_home
