#!/bin/bash
git config --global --add safe.directory /src/linux/kernel/linux
cd  /src/linux/kernel/linux
./build_sx_kernel.sh -c sx4000
# Check if the last command was successful (exit code 0)
if [ $? -eq 0 ]; then
    ./build_sx_kernel.sh -c sx4000 mod_prep
else
    echo "Kernel build failed, not proceeding with mod_prep"
    exit 1
fi
cd  /src/linux/kernel/bin/sx4000/arch/arm64/boot
gzip -c Image.015 > ./kernel.Image.gz && rm -rf Image.015
#Creating an output folder at the local workrepo for u-boot.artifactor image to copy the bin file
mkdir -p /src/linux/kernel/linux/output/
yes | cp -rf  kernel.Image.gz /src/linux/kernel/linux/output/
yes | cp -rf /src/linux/kernel/bin /src/linux/kernel/output/bin
yes | cp -rf /src/linux/kernel/linux/arch/arm64 /src/linux/kernel/output/arch/arm64
yes | cp -rf /src/linux/kernel/linux/include /src/linux/kernel/output/include
yes | cp -rf /src/linux/kernel/linux/scripts /src/linux/kernel/output/scripts
yes | cp -rf /src/linux/kernel/linux/Makefile /src/linux/kernel/output/Makefile

exec $@
