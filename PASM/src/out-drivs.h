#ifdef MUNIX_KERNEL

void pch(char ch, int x, int y) {
  putchar(ch, x+y*80);
}

#endif

#ifndef MUNIX_KERNEL
#include <stdio.h>

void gotoxy(int x,int y)    
{
    printf("%c[%d;%df",0x1B,y,x);
}
void pch(char ch, int x, int y) {
  gotoxy(x, y);
  putchar(ch);
}

#endif
