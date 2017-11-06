#!/bin/sh

set -e
set -u

DIR="$(dirname $0)"

dc() {
	docker-compose -p nap -f ${DIR}/docker-compose.yml $*
}

trap 'dc down ; dc rm -f' EXIT

rm -rf ${DIR}/backups
mkdir -p ${DIR}/backups

dc up -d elasticsearch
dc up -d database

echo 'lets print some logs..'

dc logs database
dc logs elasticsearch

dc logs elasticsearch

dc run --rm importer
dc run --rm db-backup
dc run --rm el-backup
