#!/bin/sh
pip install elasticsearch-loader
/usr/local/bin/elasticsearch_loader --index mahasiswa --type _doc json data_mhs.json
