#!/usr/bin/env bash
set -euo pipefail
pip install -U pip pip-tools

compile(){
	name=$1
	echo ">>> Compiling $name.in"
	CUSTOM_COMPILE_COMMAND=compile_reqs.sh pip-compile \
		$name.in \
		-o $name.txt
}

compile "base"
compile "test"
compile "development"
compile "production"
echo ">>> Compiling requirements files done!"
