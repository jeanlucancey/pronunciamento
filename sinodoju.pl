#!/usr/bin/perl -w
use strict;
use LWP::Simple;

my ($nbCellules);
my ($graine);
my ($ligneShell);

if ($ARGV[0]) {
    $nbCellules = $ARGV[0];
} else {
    $nbCellules = 73;
}

if ($ARGV[1]) {
    $graine = $ARGV[1];
} else {
    $graine = "beethoven";
}

$ligneShell = sprintf("./longtun2 %d %s 100000000 500 > resultat_longtun2.txt", $nbCellules, $graine);
system($ligneShell);

get("http://localhost:7777/dialogue/analyse-tunnel");
