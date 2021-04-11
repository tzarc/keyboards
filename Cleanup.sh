#!/bin/sh
find Development/ Rev*/ -type f -and -not -path '*reversible-kicad*' -and -not -name '*.zip' -exec dos2unix '{}' +
find Development/ Rev*/ -type f -and -not -path '*reversible-kicad*' -exec chmod -x '{}' +
find Development/ Rev*/ \( -type f -and -not -path '*reversible-kicad*' \) -and \( -name '*.py' -or -name '*.sh' \)  -exec chmod +x '{}' +
