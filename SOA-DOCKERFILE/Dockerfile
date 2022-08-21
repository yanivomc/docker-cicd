FROM yanivomc/gurdnox:soa-baseline as builder
RUN echo "Pull from Consul Environment Variables"

FROM yanivomc/gurdnox:soa-baseline as x86
RUN echo "Pull from Consul Environment Variables"
WORKDIR /build
RUN chmod +x -R soa_python &&   soa_python/scripts/build.sh && echo $?

FROM yanivomc/gurdnox:soa-x as install_x86-64
WORKDIR /install 
COPY --from=x86 /build/files ./
RUN install/soa_python/scripts/install.sh 

FROM yanivomc/gurdnox:soa-baseline as unit-test
RUN build/soa_python/scripts/qemu.sh










