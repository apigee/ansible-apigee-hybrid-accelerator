FROM google/cloud-sdk:alpine
ENV HELM_BASE_URL="https://get.helm.sh"
ENV HELM_VERSION="3.13.1"
SHELL ["/bin/ash", "-eo", "pipefail", "-c"]
RUN apk add --update --no-cache py-pip==23.1.2-r0 openssh==9.3_p2-r0
RUN python3 -m pip install --no-cache-dir \
        requests==2.25.1 \
        jsonschema==4.19.1 \
        jsonschema-specifications==2023.7.1 \
        jmespath==1.0.1 \
        kubernetes==27.2.0 \
        ansible-core==2.15.5 \
        ansible==8.5.0 && \
        ansible-galaxy collection install ansible.posix && \
        case $(uname -m) in \
        x86_64) ARCH=amd64; ;; \
        armv7l) ARCH=arm; ;; \
        aarch64) ARCH=arm64; ;; \
        ppc64le) ARCH=ppc64le; ;; \
        s390x) ARCH=s390x; ;; \
        *) echo "un-supported arch, exit ..."; exit 1; ;; \
        esac && \
        apk add --update --no-cache wget==1.21.4-r0 git==2.40.1-r0 curl==8.4.0-r0 bash==5.2.15-r5 yq==4.33.3-r4 && \
        wget --progress=dot:giga "${HELM_BASE_URL}/helm-v${HELM_VERSION}-linux-${ARCH}.tar.gz" -O - | tar -xz && \
        mv "linux-${ARCH}/helm" /usr/bin/helm && \
        chmod +x /usr/bin/helm && \
        rm -rf "linux-${ARCH}" && \
        gcloud components install kubectl
