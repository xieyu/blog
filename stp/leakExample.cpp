#include<stdlib.h>
#include<string>
using namespace std;

void fb();

void fa() {
  malloc(1024);
  void* p2 = malloc(233);
  free(p2);
  //string* s3 = new string("leak example");
  string s4 = string("abc");
  fb();
}

void fb() {
  printf("in function b");
}

int main() {
  fa();
  return 0;
}

