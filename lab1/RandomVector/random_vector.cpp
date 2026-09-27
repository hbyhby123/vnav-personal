#include "random_vector.h"
#include <cstdlib>
#include <algorithm>


RandomVector::RandomVector(int size, double max_val)
{
    for(int i = 0; i < size; i++)
    {
        double value = ((double)rand() / RAND_MAX) * max_val;
        vect.push_back(value);
    }
}


void RandomVector::print()
{
    for(double v : vect)
    {
        std::cout << v << " ";
    }
    std::cout << std::endl;
}


double RandomVector::mean()
{
    double sum = 0;

    for(double v : vect)
    {
        sum += v;
    }

    return sum / vect.size();
}


double RandomVector::max()
{
    return *std::max_element(vect.begin(), vect.end());
}


double RandomVector::min()
{
    return *std::min_element(vect.begin(), vect.end());
}


void RandomVector::printHistogram(int bins)
{
    std::vector<int> histogram(bins,0);

    for(double v : vect)
    {
        int index = v * bins;

        if(index >= bins)
            index = bins - 1;

        histogram[index]++;
    }


    for(int i = 0; i < bins; i++)
    {
        std::cout << i << ": ";

        for(int j = 0; j < histogram[i]; j++)
        {
            std::cout << "*";
        }

        std::cout << std::endl;
    }
}
