using System;

public class DSAlgorithm {
int size;
Random rnd;
public readonly int seed;

public float[,] values;

public DSAlgorithm (int n, float roughness, float falloff, int seed = -1)
{
	size = (int)Math.Pow(2, n);
	values = new float[size + 1, size + 1];
	seed = seed;

	if (seed != -1) {
		rnd = new Random(seed);
	} else
		rnd = new Random();

	values [0, 0] = (float)rnd.NextDouble();
	values [0, size] = (float)rnd.NextDouble();
	values [size, 0] = (float)rnd.NextDouble();
	values [size, size] = (float)rnd.NextDouble();

	int s = size / 2;
for (int i = 0; i < n / 2; i++) {
    maxDiff *= falloff;
    s /= 2;
}
}
}
