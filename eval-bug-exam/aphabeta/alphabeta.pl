#!/usr/bin/env perl

sub get_an_buffer
{
    $an_buffer={} unless $an_buffer;
    return sub
    {
	my $n=shift;
	return $an_buffer->{$n} if(exists($an_buffer->{$n}));

	my $an=0;
	foreach my $i (1..($n-1))
	{
	    $an+=(1/$i);
	}
	$an_buffer->{$n}=$an;
	return $an;
    }
}

sub get_bn_buffer
{
    $bn_buffer={} unless $bn_buffer;
    return sub
    {
	my $n=shift;
	return $bn_buffer->{$n} if(exists($bn_buffer->{$n}));

	my $bn=0;
	foreach my $i (1..($n-1))
	{
	    $bn+=(1/($i**2));
	}
	$bn_buffer->{$n}=$bn;
	return $bn;
    }
}

sub calculate_fstar
{
    my $an=shift;
    my $n=shift;
    return (($n - 3)/($an*($n - 1) - $n));
}

sub get_alphastar_calculator
{
    my $anb=get_an_buffer();
    $astar_buffer= {} unless $astar_buffer;
    return sub
    {
	my $n=shift;
	die "invalid effective coverage; has to be larger than 1" unless $n>1;

	return $astar_buffer->{$n} if(exists($astar_buffer->{$n}));

	my $an=$anb->($n);
	my $fs=calculate_fstar($an,$n);
	# calculate individual terms(t) and subterms(st)
	my $t1=($fs**2)*($an-($n/($n-1)));
	my $st1=$an * ( (4*($n+1)) / (($n-1)**2) );
	my $st2=2 * (($n+3)/($n-1));
	my $t2=$fs * ($st1-$st2);
	my $t3=$an * ( (8*($n+1))/($n*(($n-1)**2)) );
	my $t4= (($n**2)+$n+60)/(3*$n*($n-1));
	my $astar= ($t1 + $t2 - $t3 + $t4);
	$astar_buffer->{$n}=$astar;
	return $astar;
    }
}

sub get_betastar_calculator
{
    my $anb=get_an_buffer();
    my $bnb=get_bn_buffer();
    $bstar_buffer={} unless $bstar_buffer;
    return sub
    {
	my $n=shift;
	die "invalid effective coverage; has to be larger than 1" unless $n>1;
	return $bstar_buffer->{$n} if(exists($bstar_buffer->{$n}));
	my $an=$anb->($n);
	my $bn=$bnb->($n);
	my $fs=calculate_fstar($an,$n);

	my $t1 = ($fs**2) * ($bn - ((2*($n-1)) /(($n-1)**2)));
	my $st1= $bn * (8/($n-1));
	my $st2= $an * (4/($n*($n-1)));
	my $st3= (($n**3)+12*($n**2)-35*$n+18)/($n*(($n-1)**2));
	my $t2 = $fs*($st1-$st2-$st3);
	my $t3 = $bn * (16/($n*($n-1)));
	my $t4 = $an * (8/(($n**2)*($n-1)));
	my $st4= 2*($n**4+ 110*($n**2)-255*$n+126);
	my $st5= 9*($n**2)*(($n-1)**2);
	my $t5 = $st4/$st5;
	my $bstar= ($t1 + $t2 - $t3 + $t4 + $t5);
	$bstar_buffer->{$n}=$bstar;
	return $bstar;
    }
}

sub get_nbase_buffer
{
    my $poolsize=shift;
    $nbase_buffer={} unless($nbase_buffer);
    my $pijresolver=get_nbase_matrix_resolver(3*$poolsize,$poolsize);
    return sub
    {

	my $cov=shift;

	#### shortcut
	#die"Poolsize has to be larger than coverage; maybe decreasea maximum coverage" unless $n> $cov;
	#return $cov;
	### end shortcut

	my $key="$poolsize:$cov";
	return $nbase_buffer->{$key} if(exists($nbase_buffer->{$key}));

	my $nbase=0;
	my $minj=$cov<$poolsize?$cov:$poolsize;

	for my $k(1..$minj)
	{
	    $nbase+=$k*$pijresolver->($cov,$k);
	}

	$nbase_buffer->{$key}=$nbase;
	return $nbase_buffer->{$key};
    }
}


sub _get_pij_matrix
{
    my $maxcoverage=shift;
    my $poolsize=shift;

    my $jboundary=$maxcoverage < $poolsize ? $maxcoverage : $poolsize;

    my $matrix=[];
    for my $i(1..$maxcoverage)
    {
	$matrix->[$i][0]=0;
    }
    for my $j(1..$jboundary)
    {
	$matrix->[0][$j]=0;
    }
    $matrix->[0][0]=1;

    for my $i(1..$maxcoverage)
    {
	for my $j (1..$jboundary)
	{
	    my $t1= ((1+$poolsize-$j)/$poolsize)*($matrix->[$i-1][$j-1]);
	    my $t2=($j/$poolsize)*($matrix->[$i-1][$j]);
	    my $pij=$t1+$t2;
	    $matrix->[$i][$j]=$pij;
	}
    }
    return $matrix;
}

sub get_nbase_matrix_resolver
{
    my $maxcoverage=shift;
    my $poolsize=shift;
    my $matrix=_get_pij_matrix($maxcoverage,$poolsize);

    return sub
    {
	my $C=shift;
	my $k=shift;
	unless(exists($matrix->[$C][$k]))
	{
	    $matrix=_get_pij_matrix(3*$C,$poolsize);
	}
	return $matrix->[$C][$k];
    }
}

my $alphastarcalc=get_alphastar_calculator();
my $betastarcalc=get_betastar_calculator();

for my $i(11..100)
{
    my $n = $i / 10.0;
    # if ($i == 20 or $i == 30) {
    #     next
    # }
    if ($i == 30) {
        print "$n\n";
        next
    }


    my $nbase_buffer=get_nbase_buffer($n);
    my $averagen=$nbase_buffer->($n,100);
    my $alphastar=$alphastarcalc->($n);
    my $betastar=$betastarcalc->($n);
    print "$n, $averagen, $alphastar, $betastar\n";
}
