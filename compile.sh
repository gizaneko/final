#!/bin/bash

gcc ControlApp.c shmem.c -o App
gcc -shared -fPIC shmem.c -o shmem.so
gcc -shared -fPIC i2c.c -o i2c.so
make a.out
make b.out
