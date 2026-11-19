#!/bin/bash

# Install AWS CLI v2
# https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

if ! which aws > /dev/null; then
  sudo apt-get install --yes -q curl unzip

  aws_cli_temp_dir=$(mktemp -d)

  curl \
    --fail \
    --silent \
    --show-error \
    --location \
    "https://awscli.amazonaws.com/awscli-exe-linux-$(uname -m).zip" \
    --output "${aws_cli_temp_dir?}/awscliv2.zip"

  unzip -q "${aws_cli_temp_dir?}/awscliv2.zip" -d "${aws_cli_temp_dir?}"

  sudo "${aws_cli_temp_dir?}/aws/install" --update

  rm -rf "${aws_cli_temp_dir?}"
fi
