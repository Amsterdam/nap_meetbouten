#!/bin/sh

set -e
set -u

DIR="$(dirname $0)"

function dc {
	docker-compose -f ${DIR}/docker-compose.yml $*
}

mkdir -p ${DIR}/backups

dc build
dc up -d database elasticsearch

dc run --rm importer
dc run --rm db-backup > ${DIR}/backups/database.sql
dc run --rm el-backup

docker cp $(docker-compose ps -q elasticsearch):/tmp/backups ${DIR}/backups/elastic

#dc down
