#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// ============================================================
// DEMO 1: BUFFER OVERFLOW
// Vulnerability: strcpy does not check destination buffer size
// Fix: strncpy with explicit size limit
// ============================================================

void vulnerable_buffer_overflow(char *input) {
    char buffer[16];
    strcpy(buffer, input);  // VULNERABLE: no bounds check
    printf("[VULN] Buffer contains: %s\n", buffer);
}

void safe_buffer_overflow(char *input) {
    char buffer[16];
    strncpy(buffer, input, sizeof(buffer) - 1);  // SAFE: bounded copy
    buffer[sizeof(buffer) - 1] = '\0';            // ensure null termination
    printf("[SAFE] Buffer contains: %s\n", buffer);
}

// ============================================================
// DEMO 2: FORMAT STRING VULNERABILITY
// Vulnerability: user input passed directly as format string
// Fix: always use a fixed format string like %s
// ============================================================

void vulnerable_format_string(char *input) {
    printf(input);   // VULNERABLE: attacker controls format string
    printf("\n");
}

void safe_format_string(char *input) {
    printf("%s\n", input);  // SAFE: fixed format string
}

// ============================================================
// DEMO 3: USE AFTER FREE
// Vulnerability: accessing memory after it has been freed
// Fix: set pointer to NULL immediately after free
// ============================================================

void vulnerable_use_after_free() {
    char *ptr = (char *)malloc(64);
    strcpy(ptr, "sensitive bank data");
    printf("[VULN] Before free: %s\n", ptr);
    free(ptr);
    printf("[VULN] After free (undefined behaviour): %s\n", ptr); // VULNERABLE
}

void safe_use_after_free() {
    char *ptr = (char *)malloc(64);
    strcpy(ptr, "sensitive bank data");
    printf("[SAFE] Before free: %s\n", ptr);
    free(ptr);
    ptr = NULL;  // SAFE: nullify pointer immediately after free
    if (ptr != NULL) {
        printf("%s\n", ptr);
    } else {
        printf("[SAFE] Pointer is NULL after free - access blocked\n");
    }
}

// ============================================================
// MAIN: Run all demos
// ============================================================

int main() {
    printf("\n==============================\n");
    printf("  BUFFER OVERFLOW DEMO\n");
    printf("==============================\n");
    printf("Input: 'AAAAAAAAAAAAAAAAAAAAAAAAAAAA' (28 chars into 16-byte buffer)\n\n");
    vulnerable_buffer_overflow("AAAAAAAAAAAAAAAAAAAAAAAAAAAA");
    safe_buffer_overflow("AAAAAAAAAAAAAAAAAAAAAAAAAAAA");

    printf("\n==============================\n");
    printf("  FORMAT STRING DEMO\n");
    printf("==============================\n");
    printf("Input: '%%x %%x %%x' (attacker reads stack memory)\n\n");
    printf("[VULN] Output: ");
    vulnerable_format_string("%x %x %x");
    printf("[SAFE] Output: ");
    safe_format_string("%x %x %x");

    printf("\n==============================\n");
    printf("  USE AFTER FREE DEMO\n");
    printf("==============================\n\n");
    vulnerable_use_after_free();
    safe_use_after_free();

    printf("\n[DONE] All memory safety demos complete.\n\n");
    return 0;
}
