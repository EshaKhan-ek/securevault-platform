#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void safe_buffer_overflow(char *input) {
    char buffer[16];
    strncpy(buffer, input, sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';
    printf("[SAFE] Buffer contains: %s\n", buffer);
    printf("[SAFE] Input truncated to 15 chars - no overflow possible\n");
}

void safe_format_string(char *input) {
    printf("%s\n", input);
    printf("[SAFE] Format string attack neutralised - input treated as data only\n");
}

void safe_use_after_free() {
    char *ptr = (char *)malloc(64);
    strcpy(ptr, "sensitive bank data");
    printf("[SAFE] Before free: %s\n", ptr);
    free(ptr);
    ptr = NULL;
    if (ptr != NULL) {
        printf("%s\n", ptr);
    } else {
        printf("[SAFE] Pointer is NULL after free - access blocked\n");
    }
}

int main() {
    printf("\n==============================\n");
    printf("  BUFFER OVERFLOW - SAFE\n");
    printf("==============================\n");
    safe_buffer_overflow("AAAAAAAAAAAAAAAAAAAAAAAAAAAA");

    printf("\n==============================\n");
    printf("  FORMAT STRING - SAFE\n");
    printf("==============================\n");
    safe_format_string("%x %x %x");

    printf("\n==============================\n");
    printf("  USE AFTER FREE - SAFE\n");
    printf("==============================\n");
    safe_use_after_free();

    printf("\n[DONE] All mitigations working correctly.\n\n");
    return 0;
}
