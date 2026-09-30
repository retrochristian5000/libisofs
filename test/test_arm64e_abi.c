/*
 * Compile-time probe for the public callback ABI on Apple arm64e.
 *
 * This intentionally does not strip, sign, or integerize function pointers.
 * The arm64e ABI and Clang own pointer authentication at these typed
 * boundaries.  The test is compiled with strict function-pointer warnings
 * and its LLVM IR is checked for ptrauth call metadata by CI.
 */

#define HAVE_STDINT_H 1
#include <sys/types.h>
#include <time.h>

#include "libisofs/libisofs.h"

int libisofs_arm64e_ds_open(IsoDataSource *src)
{
    return src != NULL;
}

int libisofs_arm64e_ds_close(IsoDataSource *src)
{
    return src != NULL;
}

int libisofs_arm64e_ds_read(IsoDataSource *src, uint32_t lba, uint8_t *buffer)
{
    (void) lba;
    return src != NULL && buffer != NULL;
}

void libisofs_arm64e_ds_free(IsoDataSource *src)
{
    (void) src;
}

int libisofs_arm64e_xinfo(void *data, int flag)
{
    return data != NULL ? flag : 0;
}

void libisofs_arm64e_bind_data_source(IsoDataSource *src)
{
    src->open = libisofs_arm64e_ds_open;
    src->close = libisofs_arm64e_ds_close;
    src->read_block = libisofs_arm64e_ds_read;
    src->free_data = libisofs_arm64e_ds_free;
}

int libisofs_arm64e_call_data_source(IsoDataSource *src, uint8_t *buffer)
{
    int ret;

    ret = src->open(src);
    if (ret <= 0)
        return ret;

    ret = src->read_block(src, 0, buffer);
    if (src->close(src) <= 0 && ret > 0)
        ret = 0;
    return ret;
}

int libisofs_arm64e_call_xinfo(iso_node_xinfo_func fn, void *data)
{
    return fn(data, 0);
}
