FROM google/cloud-sdk:alpine

RUN apk add --update --no-cache py-pip openssh
RUN python3 -m pip install \
        requests==2.25.1 \
        jsonschema==4.19.1 \
        jsonschema-specifications==2023.7.1 \
        jmespath==1.0.1 \
        kubernetes==27.2.0 \
        ansible-core==2.15.5 \
        ansible==8.5.0

RUN ansible-galaxy collection install ansible.posix
ENV HELM_BASE_URL="https://get.helm.sh"
ENV HELM_VERSION="3.13.1"

RUN case `uname -m` in \
        x86_64) ARCH=amd64; ;; \
        armv7l) ARCH=arm; ;; \
        aarch64) ARCH=arm64; ;; \
        ppc64le) ARCH=ppc64le; ;; \
        s390x) ARCH=s390x; ;; \
        *) echo "un-supported arch, exit ..."; exit 1; ;; \
    esac && \
    apk add --update --no-cache wget git curl bash yq && \
    wget ${HELM_BASE_URL}/helm-v${HELM_VERSION}-linux-${ARCH}.tar.gz -O - | tar -xz && \
    mv linux-${ARCH}/helm /usr/bin/helm && \
    chmod +x /usr/bin/helm && \
    rm -rf linux-${ARCH}

RUN gcloud components install kubectl
