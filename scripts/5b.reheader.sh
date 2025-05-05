#!/bin/bash

bcftools reheader --header $PWD/new.header -o GCA_000003025_interim_af.vcf.gz GCA_000003025.vcf.gz
