#!/bin/bash
set -e 

VERSION="0.6.2"

TAR_FILE="ytop-${VERSION}-x86_64-unknown-linux-gnu.tar.gz"

wget "https://github.com/cjbassi/ytop/releases/download/0.6.2/${TAR_FILE}"

[ ! -e ~/bin ] && mkdir ~/bin

tar xvf "${TAR_FILE}" && \
mv ytop ~/bin/ && \
rm "${TAR_FILE}"

mkdir -p ~/.config/ytop/

cp scripts/utilities/ytop/monokai.json ~/.config/ytop/monokai.json
