#!/usr/bin/env Rscript

suppressPackageStartupMessages(require(optparse))

option_list = list(
  make_option(c("-i", "--input"), action="store", default=NA, type='character', help="input filename"),
  make_option(c("-o", "--output"), action="store", default=NA, type='character', help="output filename")
)
opt = parse_args(OptionParser(option_list=option_list))

d <- read.table(opt$input, header=F, stringsAsFactor=T, col.names=c("chr", "start", "stop", "mutations"))
d$chr <- factor(d$chr, levels = c('1'))
d <- with(d, d[order(chr),])

library(ggplot2)
pdf(opt$output)

p <- ggplot(data=d, aes(x=start, y=1)) +
  facet_grid(chr ~ ., switch='y') +
  geom_tile(aes(fill=mutations)) +
  theme(axis.title.y=element_blank(),
        axis.text.y=element_blank(),
        axis.ticks.y=element_blank(),
        strip.text.y = element_text(angle = 180)) +
  scale_fill_gradientn(colours = rainbow(5), breaks=seq(min(d$mutations),max(d$mutations),(max(d$mutations)-min(d$mutations))/4))

print(p)
dev.off()
