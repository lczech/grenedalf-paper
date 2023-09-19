At the moment, grenedalf suffers from the normal unix limit of having at max ~1000 files open at the same time
(all other tools that we know of have the same issue though). In the future, I'll write a merge command
that can work around this limiation... but for now, we have to pre-process the files in batches instead.

So first, we run three batches of ~800 files, and turn those into three sync files, which will then be fed
into grenedalf for the actual fst computation. Easy.
