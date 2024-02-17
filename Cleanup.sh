#!/bin/bash

set -e

SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
cd "${SCRIPT_DIR}"

repofind() {
    find . \( "$@" \) -and -not -path './.git/*' -and -not -path '*reversible-kicad*' -and -not -name '*.zip' -print | sort
}

# Remove executable flag on all files
repofind -type f | parallel "chmod -x '{1}'"

# Make sure scripts are executable
repofind -iname '*.sh' -or -iname '*.py' | parallel "chmod +x '{1}'"

# Convert all KiCad files to be in Unix format
repofind -type f -and \( -iname '*.kicad_*' -or -name 'fp-lib-table' -or -name 'sym-lib-table' -or -iname '*.md' -or -iname '*.svg' -or -iname '*.html' \) | parallel "dos2unix '{1}'"

# Install this script as a pre-commit hook if it's not already present
if [[ ! -L "${SCRIPT_DIR}/.git/hooks/pre-commit" ]] ; then
    (cd "${SCRIPT_DIR}/.git/hooks" && ln -sf ../../cleanup.sh pre-commit)
fi

# Drop out of "git commit" if there are any uncommitted changes after the cleanup.
if [[ ! -z "$(echo "${BASH_SOURCE[@]}" | grep "pre-commit")" ]] ; then
    [[ ! -z "$(git diff)" ]] && echo -e "\e[0;37m[\e[1;31mFAIL\e[0;37m]\e[0m Aborting commit: 'git diff' says changes are still present." && exit 1
fi

exit 0
