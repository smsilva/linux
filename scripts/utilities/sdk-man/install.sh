#!/bin/bash
checking() {
  MESSAGE=$1
  echo ""
  echo "Checking ${MESSAGE}..."
}

checking "SDKMAN"
if ! sdk --version > /dev/null; then
  curl -s "https://get.sdkman.io" | bash
  source "$HOME/.sdkman/bin/sdkman-init.sh"
fi

sdk version

checking "Java"
if ! which java > /dev/null; then
  sdk install java 17.0.9-zulu
fi

java --version

checking "Maven"
if ! which mvn > /dev/null; then
  sdk install maven
fi

mvn --version

checking "Spring Boot CLI"
if ! which spring > /dev/null; then
  sdk install springboot
fi

spring --version
