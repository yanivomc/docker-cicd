docker build  -t satixfy-repo.devopshift.com/buildroot/buildroot-cicd:1.00.0 -f buildroot.cicd.Dockerfile . 
docker build  -t satixfy-repo.devopshift.com/u-boot/u-boot-cicd:1.00.0 -f u-boot.cicd.Dockerfile .
docker push satixfy-repo.devopshift.com/u-boot/u-boot-cicd:1.00.0


docker build  -t satixfy-repo.devopshift.com/kernel/kernel-cicd:1.00.0 -f kernel.cicd.Dockerfile .
docker push satixfy-repo.devopshift.com/kernel/kernel-cicd:1.00.0




artifacts:
satixfy-repo.devopshift.com/kernel/kernel-artifact
satixfy-repo.devopshift.com/kernel/u-boot-artifact
satixfy-repo.devopshift.com/kernel/buildroot-artifact




----------
ARG KERNEL_VERSION
ARG U-BOOT_VERSION
ARG BUILDROOT_VERSION

docker build -t sw-builder --build-arg="KERNEL_VERSION=15" --build-arg="U_BOOT_VERSION=8" --build-arg="BUILDROOT_VERSION=11" -f sw.devBuilder.Dockerfile .