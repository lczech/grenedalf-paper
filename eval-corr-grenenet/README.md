# Check that the values computed with different implementations are the same

Here, we test how much the values for different estimators differ when computed with the different tools. We generally do not expect exact matches, due to numerical differences in the computation. Furthermore, in real-world data, there are typically edge cases, such as the handling of deleted positions, that cause implementations to differ. Still, we would hope for at least a decent correlation between implementation, which we test here.
