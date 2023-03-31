#!/usr/bin/python

# We want chunks of the A.thaliana genome of specific lengths, for our speed testing.
# Use the information from the TAIR reference fai to figure out which chromosomes and ranges are needed to achieve these chunks.


# chunks that we want:
# 1000 2000 5000 10000 20000 50000 100000 200000 500000 1000000 2000000 5000000 10000000 20000000 50000000 100000000

# fai:
#   1	30427671	71	79	80
#   2	19698289	30812975	79	80
#   3	23459830	50760682	79	80
#   4	18585056	74517544	79	80
#   5	26975502	93337926	79	80
#   mitochondria	366924	120654974	79	80
#   chloroplast	154478	121026625	79	80

fai = [ 30427671, 19698289, 23459830, 18585056, 26975502 ]

chunks = [ 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000, 2000000, 5000000, 10000000, 20000000, 50000000, 100000000 ]

with open('ref_lengths.txt', 'w') as f:
    for target in chunks:
        sum = 0
        regions = ""
        for i in range(0, 5):
            c = i+1
            if sum + fai[i] > target:
                regions += " " + str(c) + ":1-" + str( target - sum )
                break
            regions += " " + str(c) + ":1-" + str( fai[i] )
            sum += fai[i]
        print( target, regions.strip() )
        f.write( str(target) + "\t" + regions.strip() + "\n")
