#include <stdio.h>

#include "dmtcp.h"

void dmtcpc_checkpoint(char* string) {
    int ret = dmtcp_checkpoint();
    if (ret < 0) {
      printf("Error creating checkpoint!.\n");
    }
}
