#include "pasm.h"
#include <stdio.h>
#include <stdlib.h>

#define MAX_LEN 20
#define MAX_INS 65536

VMachine mach;

void compile_run(const char *file) {
  FILE *f = fopen(file, "r");
  char buffer[MAX_LEN];
  int instructions[MAX_INS];
  int time = 0;
  while (fgets(buffer, MAX_LEN, f)) {
    strtok(buffer, '\n');
    instructions[time] = asemble(buffer);
    if (asemble(buffer) == -1) {
      break;
    }
    time++;
  }
  init_mach(&mach);
  while (mach.counter < time) {
    exec(instructions[mach.counter], &mach);
    mach.counter++;
  }
}
