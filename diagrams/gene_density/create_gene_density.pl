use Data::Dumper;
use Bio::EnsEMBL::Registry;
Bio::EnsEMBL::Registry->load_registry_from_db(
	-host => 'mysql-ens-sta-1',
	-user => 'ensro',
	-port => 4519,
	-db_version => 114
  );

$input_file = "gene_count.tsv";
$gene_adaptor = Bio::EnsEMBL::Registry->get_adaptor( "pig", "core", "gene" );

open($fh, "<", $input_file) or die "cannot open file $input_file - $!\n";
@gene_density;
#$i = 0;
while(<$fh>){
	chomp;
	#print $_, "\n";
	($stable_id, $count) = split(/\t/);

	$gene = $gene_adaptor->fetch_by_stable_id($stable_id);

	if ($gene) {
		$density = $count / ($gene->seq_region_end - $gene->seq_region_start);
		push @gene_density, [$stable_id, $count, $density];
	}
	else {
		print("Cannot find gene - $stable_id\n");
	}
	#last if $i >= 5;
	#$i += 1;
}
#print Dumper \@gene_density, "\n";
close $fh;

@sorted_gene_density = sort {$b->[2] <=> $a->[2]} @gene_density;
#print Dumper \@sorted_gene_density, "\n";

$output_file = "gene_density.tsv";
open($fh, ">", $output_file) or die "cannot open file $output_file - $!\n";
foreach (@sorted_gene_density) {
	print $fh $_->[0]."\t".$_->[1]."\t".$_->[2]."\n";
}
close $fh;
