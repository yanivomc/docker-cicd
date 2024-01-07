<!-- Testing SW: -->
time docker run -ti   -v $(pwd):/home/vagrant/proj/t_branch_sw_tree_05_07_23_release_20_6/SW  satixfy-repo.devopshift.com/swdevbuilder/swdevbuilder-artifact:11 build
<!-- From vscode: -->
time docker run -ti   -v /home/vagrant/work/t_branch_sw_tree_05_07_23_newer/SW-TEST1:/home/vagrant/proj/t_branch_sw_tree_05_07_23_release_20_6/SW  satixfy-repo.devopshift.com/swdevbuilder/swdevbuilder-artifact:11 build

<!-- Add Build argument to also build -->



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




-----
VSCODE

mkdir -p ~/.config
docker run -d  --rm --name code-server -p 0.0.0.0:5005:8080 \
  -v "$HOME/.config:/home/coder/.config" \
  -v "$PWD:/home/coder/project" \
  -u "$(id -u):$(id -g)" \
  -e "DOCKER_USER=$USER" \
  codercom/code-server:latest
