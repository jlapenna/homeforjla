#!/bin/bash

source tools/scripts/base.sh

function main() {
  repo_path=$(readlink -e "$PWD")

  local install_path=$1
  if [ -z "${install_path}" ]; then
    install_path="."
  fi
  install_path=$(readlink -e "$install_path")

  local configurations_path="${install_path}/assistant-relay/server/configurations"
  local config_path="${configurations_path}/config.json"
  local key_file_path="${configurations_path}/secrets/homeforjla.json"
  local saved_tokens_path="${configurations_path}/tokens/homeforjla-tokens.json"

  pushd $install_path

  if [[ ! -d "assistant-relay" ]]; then
    echo "Installing pre-reqs"
    sudo npm i pm2
    echo ""
    echo "Please download a release to ~/assistant-relay.zip:"
    echo "  https://github.com/greghesp/assistant-relay/releases"
    mkdir assistant-relay
    unzip assistant-relay.zip -d assistant-relay
    pushd assistant-relay
    npm install
    echo ""
    echo "Be sure to 'npm run start then visit port 3000'"
    popd
  else
    echo "Pulling and rebasing repo."
    pushd assistant-relay
    popd
  fi

  echo "Setting up service."
  sudo cp ${repo_path}/raspberrypi/assistant_relay/assistant_relay.service \
      /lib/systemd/system/
  sudo systemctl enable assistant_relay
  curl -d '{"command":"hello world", "user":"homeforjla", "broadcast":"true"}' \
      -H "Content-Type: application/json" -X POST \
      "http://raspberrypi.lan:3000/assistant"

  popd
  popd
}

main "$@"
