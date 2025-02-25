#!/bin/bash

COPR_WEBHOOK=$1

thirdparty_pkgs_array=('ghostty' 'python-neovim' 'rust-tealdeer' 'utf8proc' 'wezterm' 'zed' 'zed-preview')

for file in "${thirdparty_pkgs_array[@]}"; do
	echo "Processing file: $file"
	curl -X POST "$COPR_WEBHOOK/$file/"
done
