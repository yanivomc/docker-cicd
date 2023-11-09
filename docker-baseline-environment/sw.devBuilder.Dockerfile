# Docker build file for Dev environment and CI/CD Pipeline
# This will prepare all the required artifacts for the developer per the version specified/latest version of Kernel, U-Boot and Buildroot


#To run this on local env - # Mount local dev folder to: /home/vagrant/proj/t_branch_sw_tree_05_07_23_release_20_6/SW and run 
#PWD is the local folder of your SW project (e.g. /home/vagrant/proj/t_branch_sw_tree_05_07_23_release_20_6/SW)
# docker run -it --rm -v $(pwd):/home/vagrant/proj/t_branch_sw_tree_05_07_23_release_20_6/SW satixfy-repo.devopshift.com/sw/dev:latest
ARG KERNEL_VERSION=latest
ARG U_BOOT_VERSION=latest
ARG BUILDROOT_VERSION=latest
FROM satixfy-repo.devopshift.com/kernel/kernel-artifact:$KERNEL_VERSION AS kernel-builder
FROM satixfy-repo.devopshift.com/u-boot/u-boot-artifact:$U_BOOT_VERSION AS u-boot-builder
FROM satixfy-repo.devopshift.com/buildroot/buildroot-artifact:$BUILDROOT_VERSION AS root-builder


FROM satixfy-repo.devopshift.com/buildtools/buildtools:1.00.0 AS sw-builder
RUN apt update && apt-get install -y device-tree-compiler make gcc gcc-multilib g++ mtd-utils rsync

WORKDIR /SW

WORKDIR /workarea/SW/bin/sx4000/images_tmp
COPY --from=kernel-builder /src/linux/kernel/output/kernel.Image.gz ./kernel.Image.gz
COPY --from=u-boot-builder /src/linux/u-boot/bin/sx4000/u-boot.bin ./u-boot.bin
COPY --from=root-builder /src/linux/buildroot/output/sx4000/images/rootfs.squashfs.partition ./rootfs.squashfs.partition
WORKDIR /workarea/linux/
COPY --from=root-builder /src/linux/buildroot/output/sx4000/host/aarch64-buildroot-linux-gnu/sysroot ./buildroot/output/sx4000/host/aarch64-buildroot-linux-gnu/sysroot
COPY --from=kernel-builder /src/linux/kernel/output/bin ./kernel/bin
COPY --from=kernel-builder /src/linux/kernel/output/arch/arm64 ./kernel/linux/arch/arm64
COPY --from=kernel-builder /src/linux/kernel/output/include ./kernel/linux/include
COPY --from=kernel-builder /src/linux/kernel/output/scripts ./kernel/linux/scripts
COPY --from=kernel-builder /src/linux/kernel/output/Makefile ./kernel/linux/Makefile


WORKDIR /workarea/SW/build
ENV SKIP_KERNEL=1
ENV SKIP_UBOOT=1
ENV SKIP_BUILDROOT=1
WORKDIR /workarea/
COPY ./sw.devBuilderEntrypoint.sh /entrypoint.sh
