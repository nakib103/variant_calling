module add nextflow/23.04.1

bsub -J sarek -oo sarek.out -eo sarek.err -M7000 "nextflow run ../sarek \
	-profile singularity \
	--input ../configs/PRJNA186497.csv \
	--fasta ../inputs/GCA_000472085/GCA_000472085.2.fasta.gz \
	--outdir ../outputs/GCA_000472085"
