#include <stdio.h>
#include <stdlib.h>
#include "./sdk/include/Everything.h"

int search(char *name) {
    system("chcp 936");
    printf("Search: %s\n", name);
    Everything_SetSearch(name);

    return Everything_Query(TRUE);
}

DWORD getResultNum() {
    return Everything_GetNumResults();
}

LPCTSTR getResult(DWORD i) {
    system("chcp 936");
    printf("Result: %s\n", Everything_GetResultFileName(i));

    return Everything_GetResultFileName(i);
}
