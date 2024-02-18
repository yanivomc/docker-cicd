#!/bin/bash

echo "Running sw.devBuilderEntrypoint.sh"
echo "Copying LINUX artifacts to local developer environment"
cp -R /workarea/linux /home/vagrant/proj/t_branch_sw_tree_05_07_23_release_20_6/linux
echo "Copying  SW artifacts to local developer environment"
cp -R /workarea/SW/* /home/vagrant/proj/t_branch_sw_tree_05_07_23_release_20_6/SW/
echo "Removing imgtxt2enum.d from local developer environment"
rm -rf /home/vagrant/proj/t_branch_sw_tree_05_07_23_release_20_6/SW/Tools/eldan_utils/imgtxt2enum.d

#Run Build:
# Check if user added argument build and if so exec build
if [ "$1" == "build" ]; then
    echo "Build argument found, executing build"
    cd /home/vagrant/proj/t_branch_sw_tree_05_07_23_release_20_6/SW/build
    source /devtools/eldan_env.sh &&  ./build_all.sh linux_bundle sx4000 ceva_no_opt
else
    echo "No build argument found, skipping build only copying required artifacts to local SW folder"
fi