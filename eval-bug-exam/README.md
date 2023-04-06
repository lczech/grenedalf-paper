This directory contains some tests to determine the effects of the two bugs in PoPoolation
that affect the numerical values of the pool-correct variant of Tajima's D.

In short, we find that while the values can differ by up to an order of magnitude from the
correct ones, they do so in a consistent manner. That is, for given settings of minimum
coverage and pool size, the deviation of Tajima's D is off by a factor that is more or
less consitent, so that it is improbable that interpretations based on relative peaks
of Tajima's D are wrong. Absolute values obtain with the PoPoopulation versions that
contain the bug (<= 1.2.2) should not be used for interpreting the data though.

For larger values of min coverage and pool size however, and in particular for larger window
sizes that contain more SNPs, the effect of the bugs gets smaller, so that typical analyses
might not even be affect all too much.

Lastly, this directory also contains a test of the alpha-star and beta-star functions
to determine their behaviour for low input values of n, and for float instead of integer
input for these functions.
