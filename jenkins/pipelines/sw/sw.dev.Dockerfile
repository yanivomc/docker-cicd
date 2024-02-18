# Docker build file for Dev environment
# This will prepare all the required artifacts for the developer per the version specified
# then the developer will run docker run to copy all artifacts to local machine and run build_all.sh
ARG KERNEL_VERSION
ARG U_BOOT_VERSION
ARG BUILDROOT_VERSION
FROM eldan-repo.devopshift.com/kernel/kernel-artifact:$KERNEL_VERSION AS kernel-builder
FROM eldan-repo.devopshift.com/u-boot/u-boot-artifact:$U_BOOT_VERSION AS u-boot-builder
FROM eldan-repo.devopshift.com/buildroot/buildroot-artifact:$BUILDROOT_VERSION AS root-builder


FROM eldan-repo.devopshift.com/buildtools/buildtools:1.00.0 AS sw-builder
RUN apt update && apt-get install -y device-tree-compiler make gcc gcc-multilib g++ mtd-utils rsync
# Move the below command into entrypoint as it needs to run on DOCKER run and not build




# Mount local dev folder to: /home/vagrant/proj/t_branch_sw_tree_05_07_23_release_20_6/SW
WORKDIR /home/vagrant/proj/t_branch_sw_tree_05_07_23_release_20_6/SW
# COPY . ./SW/
RUN rm -rf ./SW/Tools/eldan_utils/imgtxt2enum.d
#WORKDIR /src/SW
# Copy all required artifacts to project folder (this will expose on local dev machine)
WORKDIR /home/vagrant/proj/t_branch_sw_tree_05_07_23_release_20_6/SW/bin/sx4000/images_tmp
COPY --from=kernel-builder /src/linux/kernel/output/kernel.Image.gz ./kernel.Image.gz
COPY --from=u-boot-builder /src/linux/u-boot/bin/sx4000/u-boot.bin ./u-boot.bin
COPY --from=root-builder /src/linux/buildroot/output/sx4000/images/rootfs.squashfs.partition ./rootfs.squashfs.partition
WORKDIR /home/vagrant/proj/t_branch_sw_tree_05_07_23_release_20_6/linux/
COPY --from=root-builder /src/linux/buildroot/output/sx4000/host/aarch64-buildroot-linux-gnu/sysroot ./buildroot/output/sx4000/host/aarch64-buildroot-linux-gnu/sysroot
COPY --from=kernel-builder /src/linux/kernel/output/bin ./kernel/bin
COPY --from=kernel-builder /src/linux/kernel/output/arch/arm64 ./kernel/linux/arch/arm64
COPY --from=kernel-builder /src/linux/kernel/output/include ./kernel/linux/include
COPY --from=kernel-builder /src/linux/kernel/output/scripts ./kernel/linux/scripts
COPY --from=kernel-builder /src/linux/kernel/output/Makefile ./kernel/linux/Makefile


#WORKDIR /src/SW/build
WORKDIR /home/vagrant/proj/t_branch_sw_tree_05_07_23_release_20_6/SW/build
ENV SKIP_KERNEL=1
ENV SKIP_UBOOT=1
ENV SKIP_BUILDROOT=1
## Unmark when we wish to allow it to build


#RUN source /devtools/eldan_env.sh &&  ./build_all.sh linux_bundle sx4000 ceva_no_opt


WORKDIR /devtools/
