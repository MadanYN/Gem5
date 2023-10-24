#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define N 5

int main(){
    // bool isPrime[N+1];
    bool *isPrime = (bool*)malloc((N+1) * sizeof(bool));
    if (isPrime == NULL) {
        perror("Memory allocation failed");
        return 1;
    }
    for(int i = 2; i <= N ; i++){
        isPrime[i] = true;
    }

    for(int p = 2; p*p <= N; p++){
        if(isPrime[p] == true){
            for(int i = p*p; i <= N; i += p){
                isPrime[i] = false;
            }
        }
    }
    long count = 0;
    for(int i = 2; i <= N; i++){
        if(isPrime[i]){
            count++;
        }
    }

    printf("Number of primes less than %d is %ld\n", N, count);
}