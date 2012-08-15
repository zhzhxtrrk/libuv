

#include "uv.h"

#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

uv_signal_t sigint, sigbreak, sigterm;


void signal_cb(uv_signal_t* handle, int signum) {
  printf("Signal: %d\n", signum);
}


int main(int argc, char* argv[]) {
  
  uv_signal_init(uv_default_loop(), &sigint);
  uv_signal_start(&sigint, signal_cb, SIGINT);

  uv_signal_init(uv_default_loop(), &sigbreak);
  uv_signal_start(&sigbreak, signal_cb, SIGBREAK);

  uv_signal_init(uv_default_loop(), &sigterm);
  uv_signal_start(&sigterm, signal_cb, SIGHUP);

  uv_run(uv_default_loop());

  return 0;
}