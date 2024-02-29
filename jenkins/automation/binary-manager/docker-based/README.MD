# Uploader cli:
~~~
docker run -ti -v /tmp/demo-uploader:/resources --env FILE_PATH=/resources/ceva.dll --env NEXUS_REPO_PROJECT=ceva-3.00 --env NEXUS_USER=$NEXUS_USER --env NEXUS_PASSWORD=$NEXUS_PASSWORD --env NEXUS_BASE_URL=$NEXUS_BASE_URL --env BUILD_NUMBER=3.00 yanivomc/uploader
~~~

## Arguments required as env variable:
NEXUS_BASE_URL      NEXUS_PASSWORD      NEXUS_REPO_PROJECT  NEXUS_USER  BUILD_NUMBER

ex.:
NEXUS_BASE_URL: https://eldan-repo.devopshift.com/nexus/repository/eldanrepo
NEXUS_REPO_PROJECT: ceva-1.00  


NEXUS_REPO_PROJECT Is the FOLDER!!

