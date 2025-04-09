#!/bin/bash

case "$1" in
  setup)
    exec bash /app/quickstart.sh
    ;;
  *)
    exec contentgen "$@"
    ;;
esac
