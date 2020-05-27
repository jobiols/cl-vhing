#!/usr/bin/env bash

sudo docker run --rm -it \
    --link aeroo:aeroo \
    --link wdb \
    -p 8888:3001 \
    -p 8069:8069 \
    -p 8072:8072 \
    -v /odoo_ar/odoo-11.0/vhing/config:/opt/odoo/etc/ \
    -v /odoo_ar/odoo-11.0/vhing/data_dir:/opt/odoo/data \
    -v /odoo_ar/odoo-11.0/vhing/log:/var/log/odoo \
    -v /odoo_ar/odoo-11.0/vhing/sources:/opt/odoo/custom-addons \
    -v /odoo_ar/odoo-11.0/vhing/backup_dir:/var/odoo/backups/ \
    -v /odoo_ar/odoo-11.0/extra-addons:/opt/odoo/extra-addons \
    -v /odoo_ar/odoo-11.0/dist-packages:/usr/lib/python3/dist-packages \
    -v /odoo_ar/odoo-11.0/dist-local-packages:/usr/local/lib/python3.5/dist-local-packages \
    --link pg-vhing:db \
    --name vhing-vscode \
    -e ODOO_CONF=/dev/null \
    -e SERVER_MODE=test \
    -e WDB_SOCKET_SERVER=wdb \
    jobiols/odoo-jeo:11.0.debug \
    /usr/bin/python3 -m debugpy --listen 0.0.0.0:3001 /usr/bin/odoo
    --logfile=/dev/stdout
