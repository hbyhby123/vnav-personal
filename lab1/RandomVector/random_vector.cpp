#include "random_vector.h"
#include <cstdlib>


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
    double max_value = vect[0];

    for(double v : vect)
    {
        if(v > max_value)
        {
            max_value = v;
        }
    }

    return max_value;
}


double RandomVector::min()
{
    double min_value = vect[0];

    for(double v : vect)
    {
        if(v < min_value)
        {
            min_value = v;
        }
    }

    return min_value;
}


void RandomVector::printHistogram(int bins)
{
    if (bins <= 0 || vect.empty())
        return;

    double low = min();
    double high = max();
    std::vector<int> histogram(bins, 0);

    for (double v : vect)
    {
        int index = 0;
        if (high > low)
        {
            index = static_cast<int>(
                (v - low) / (high - low) * bins);
            if (index >= bins)
                index = bins - 1;
        }
        histogram[index]++;
    }

    int height = 0;
    for (int count : histogram)
    {
        if (count > height)
            height = count;
    }

    for (int row = height; row > 0; row--)
    {
        for (int i = 0; i < bins; i++)
        {
            if (histogram[i] >= row)
                std::cout << "***";
            else
                std::cout << "   ";

            if (i < bins - 1)
                std::cout << " ";
        }
        std::cout << std::endl;
    }
}
