/* jshint esversion: 6 */
"use strict";

function isPrime(n) {
    for (let i = 2; i < n / 2 + 1; i++) {
        if (n % i === 0) {
            return false;
        }
    }
    return true;
}

function getNPrimes(n) {
    var i = 2;
    var lst = [];
    while (true) {
        if (isPrime(i)) {
            lst.push(i);
        }
        i = i + 1;
        if (lst.length >= n) {
            return lst;
        }
    }
}

