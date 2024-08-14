FROM yanivomc/jenkins-slave:baseline
RUN pip install jenkins-webapi
RUN powershell -Command \
    Invoke-WebRequest -UseBasicParsing -Uri "https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-windows-x86_64.exe" -OutFile C:\Windows\System32\docker-compose.exe
RUN mkdir -p /home/jenkins
RUN mkdir -p /var/lib/jenkins

# Start-up script to attach the slave to the master
ADD slave.py /var/lib/jenkins/slave.py

WORKDIR /home/jenkins

ENV JENKINS_URL "https://eldan-repo.devopshift.com/jenkins/"
ENV JENKINS_SLAVE_ADDRESS ""
ENV JENKINS_USER "admin"
ENV JENKINS_PASS "admin"
ENV SLAVE_NAME ""
ENV SLAVE_SECRET ""
ENV SLAVE_EXECUTORS "1"
ENV SLAVE_LABELS "windows"
ENV SLAVE_WORING_DIR ""
ENV CLEAN_WORKING_DIR "true"

CMD [ "python3", "-u", "c:\var\lib\jenkins\slave.py" ]

