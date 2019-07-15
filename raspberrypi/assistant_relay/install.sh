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
    echo "Cloning and updating repo."
    git clone https://github.com/greghesp/assistant-relay.git
    pushd assistant-relay
    git checkout -b production
    sed -i 's/"google-assistant": "^0.2.0"/"google-assistant": "^0.5.4"/g' package.json
    npm install
    npm audit fix
    git commit -a -m'Update google-assistant configuration'
  else
    echo "Pulling and rebasing repo."
    pushd assistant-relay
    git pull origin master
    git rebase master
  fi

  echo "Copying secrets and configs."
  cp ${repo_path}/raspberrypi/assistant_relay/config.json ${config_path} 
  cp ${repo_path}/private/raspberrypi/assistant_relay/homeforjla.json ${key_file_path}
  cp ${repo_path}/private/raspberrypi/assistant_relay/homeforjla_tokens.json ${saved_tokens_path}
  sed \
      -e "s#INSTALL_PATH#${install_path}#g" \
      -i ${config_path};
  git commit -a -m'Update configuration and client secrets.'

  popd
  popd
}

main "$@"
