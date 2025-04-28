#!/bin/bash

data_dir=$PWD/../data
out_dir=$PWD/../outputs

time docker run \
-v "$data_dir":"/data" \
cgrlab/glnexus:v1.4.1 \
glnexus_cli \
--config DeepVariantWGS \
--list /data/GLnexus.manifest \
| bcftools view - \
| bgzip -c \
| $out_dir/deepvariant.cohort.vcf.gz
