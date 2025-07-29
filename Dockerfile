FROM google/cloud-sdk:532.0.0-alpine
ENV HELM_BASE_URL="https://get.helm.sh"
ENV HELM_VERSION="3.14.2"
SHELL ["/bin/ash", "-eo", "pipefail", "-c"]
RUN apk add --update --no-cache py3-pip==24.0-r2 && \
    python3 -m pip install --no-cache-dir \
        requests==2.32.4 \
        jsonschema==4.25.0 \
        jsonschema-specifications==2025.4.1 \
        jmespath==1.0.1 \
        kubernetes==33.1.0 \
        oauth2client==4.1.3 \
        ansible==11.8.0 \
        ansible-core==2.18.7 --break-system-packages && \
    ansible-galaxy collection install ansible.posix && \
    ansible-galaxy collection install ansible.utils && \
    case $(uname -m) in \
        x86_64) ARCH=amd64; ;; \
        armv7l) ARCH=arm; ;; \
        aarch64) ARCH=arm64; ;; \
        ppc64le) ARCH=ppc64le; ;; \
        s390x) ARCH=s390x; ;; \
        *) echo "un-supported arch, exit ..."; exit 1; ;; \
        esac && \
    apk add --update --no-cache \
        wget==1.24.5-r0 \
        git==2.45.4-r0 \
        curl==8.12.1-r0 \
        bash==5.2.26-r0 \
        yq-go==4.44.1-r2 && \
    wget --progress=dot:giga "${HELM_BASE_URL}/helm-v${HELM_VERSION}-linux-${ARCH}.tar.gz" -O - | tar -xz && \
    mv "linux-${ARCH}/helm" /usr/bin/helm && \
    chmod +x /usr/bin/helm && \
    rm -rf "linux-${ARCH}" && \
    gcloud components install kubectl
