#include <stdio.h>

// FIX: Correct the logic in the multiplyNums function
// TODO: Implement error handling for invalid inputs

void multiplyNums(int a, int b) {
    // REVISIT: Review and optimise
    int mult = a * b;
    printf("Total: %d\n", mult);
}

int main() {
    // BUG: This variable isnt being updated correctly
    double num_1 = 1000.0;
    double num_2 = 0.05;

    MultiplyNums(num_1, num_2);
    return 0;
}