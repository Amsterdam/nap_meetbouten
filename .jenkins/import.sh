#!/bin/sh

set -e
set -u

DIR="$(dirname $0)"

function dc {
	docker-compose -f ${DIR}/docker-compose.yml $*
}

trap 'dc down' EXIT

rm -rf ${DIR}/backups
mkdir -p ${DIR}/backups

dc build
dc run --rm importer
dc run --rm db-backup
dc run --rm el-backup

