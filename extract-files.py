#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.file import File
from extract_utils.fixups_blob import (
    BlobFixupCtx,
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    "device/xiaomi/sm8250-common",
    "hardware/qcom-caf/common/libqti-perfd-client",
    "hardware/qcom-caf/sm8250",
    "hardware/qcom-caf/wlan",
    "hardware/xiaomi",
    "vendor/qcom/opensource/commonsys/display",
    "vendor/qcom/opensource/commonsys-intf/display",
    "vendor/qcom/opensource/dataservices",
    "vendor/qcom/opensource/display",
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        "com.qualcomm.qti.dpm.api@1.0",
        "libmmosal",
        "vendor.qti.hardware.wifidisplaysession@1.0",
        "vendor.qti.imsrtpservice@3.0",
        "vendor.qti.ims.callcapability@1.0",
        "vendor.qti.ims.callinfo@1.0",
        "vendor.qti.ims.factory@1.0",
        "vendor.qti.ims.factory@1.1",
        "vendor.qti.ims.rcsconfig@1.0",
        "vendor.qti.ims.rcsconfig@1.1",
        "vendor.qti.ims.rcsconfig@2.0",
        "vendor.qti.ims.rcsconfig@2.1",
    ): lib_fixup_vendor_suffix,
    (
        "libOmxCore",
        "libwpa_client"
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    'vendor/etc/media_codecs_kona.xml': blob_fixup()
        .regex_replace('.+media_codecs_dolby_audio.+\n', ''),
    'system_ext/lib64/libwfdservice.so': blob_fixup()
        .replace_needed('android.media.audio.common.types-V2-cpp.so', 'android.media.audio.common.types-V4-cpp.so'),
    'system_ext/lib64/libwfdnative.so': blob_fixup()
        .add_needed('libinput_shim.so')
        .add_needed('libbinder_shim.so'),
    'system_ext/lib64/libwfdmmsrc_system.so': blob_fixup()
        .add_needed('libgui_shim.so'),
    'vendor/etc/init/init.mi_thermald.rc': blob_fixup()
        .regex_replace('.+seclabel u:r:mi_thermald:s0\n', ''),
    ('vendor/lib64/libwvhidl.so', 'vendor/lib64/mediadrm/libwvdrmengine.so'): blob_fixup()
        .add_needed('libcrypto_shim.so'),
    'vendor/etc/seccomp_policy/atfwd@2.0.policy': blob_fixup()
        .add_line_if_missing('gettid: 1'),
}  # fmt: skip

module = ExtractUtilsModule(
    'sm8250-common',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    check_elf=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()