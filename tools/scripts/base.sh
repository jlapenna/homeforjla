#!/bin/bash

function get_repo_path() {
  local repo_path=$(readlink -e "$PWD")
  if [[ "$(basename ${repo_path})" != "jlahome" ]]; then
    echo "Must be in the jlahome code repo." >&2
    return 1;
  fi
  echo "${repo_path}";
}
