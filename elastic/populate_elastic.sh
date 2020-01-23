#!/bin/sh
pip install elasticsearch-loader
elasticsearch_loader --index mahasiswa --type _doc json data_mhs.json
