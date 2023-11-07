docker build  -t satixfy-repo.devopshift.com/buildroot/buildroot-cicd:1.00.0 -f buildroot.cicd.Dockerfile . 
docker build  -t satixfy-repo.devopshift.com/u-boot/u-boot-cicd:1.00.0 -f u-boot.cicd.Dockerfile .
docker push satixfy-repo.devopshift.com/u-boot/u-boot-cicd:1.00.0


docker build  -t satixfy-repo.devopshift.com/kernel/kernel-cicd:1.00.0 -f kernel.cicd.Dockerfile .
docker push satixfy-repo.devopshift.com/kernel/kernel-cicd:1.00.0