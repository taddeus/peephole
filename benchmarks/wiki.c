#include <stdio.h>

int main(void)
{
    int a = 3, b = 5, d = 5, x = 100;
    int c = 0;
    if (a > b)
    {
        int c = a + b;
        d = 2;
    }
    
    c = 4;
    
    return b * d + c;
}
