#!/bin/bash
checking() {
  message="${1}"
  echo ""
  echo "Checking ${message}..."
}

checking "SDKMAN"
if [[ ! -e "${HOME}/.sdkman/bin/sdkman-init.sh" ]]; then
  curl -s "https://get.sdkman.io" | bash
  sed -i "s|sdkman_auto_answer=false|sdkman_auto_answer=true|" ~/.sdkman/etc/config > /dev/null
fi

source "${HOME}/.sdkman/bin/sdkman-init.sh"

sdk version

checking "Java"
if ! which java > /dev/null; then
  sdk install java 22-zulu
fi

java --version

checking "Maven"
if ! which mvn &> /dev/null; then
  sdk install maven
fi

mvn --version

checking "Spring Boot CLI"
if ! which spring &> /dev/null; then
  sdk install springboot
fi

spring --version
