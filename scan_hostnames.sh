#!/bin/bash

for ip_subset in `seq 97 123`; do
    host 10.153.101.$ip_subset
done

for ip_subset in `seq 193 251`; do
    host 10.153.101.$ip_subset
done