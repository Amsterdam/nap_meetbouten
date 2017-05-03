#!/bin/sh

set -e
set -u

DIR="$(dirname $0)"

dc() {
	docker-compose -p nap -f ${DIR}/docker-compose.yml $*
}

#trap 'dc kill ; dc rm -f' EXIT
#
#rm -rf ${DIR}/backups
#mkdir -p ${DIR}/backups

dc build
#dc run --rm importer
#dc run --rm db-backup
#dc run --rm el-backup
dc run importer
dc run db-backup
dc run el-backup
