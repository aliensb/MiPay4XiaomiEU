"""Package the Xiaomi 15 Ultra EEA module from an extracted CN product tree."""

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, BadZipFile, ZipFile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("product", type=Path, help="Extracted CN product directory")
    parser.add_argument("output", type=Path, help="Output module ZIP")
    args = parser.parse_args()

    apps = args.product / "app"
    apps_to_mount = {
        "MINextpay": "MINextpay",
        # Keep the EEA system app path so Package Manager sees one TSM package.
        "MITSMClient": "MITSMClientGlobal",
        "UPTsmService": "UPTsmService",
        "MIUISuperMarket": "MIUISuperMarket",
    }
    files = {
        f"{target}/{target}.apk": apps / source / f"{source}.apk"
        for source, target in apps_to_mount.items()
    }
    for apk in files.values():
        if not apk.is_file():
            parser.error(f"Missing {apk}")
        try:
            with ZipFile(apk) as archive:
                if "AndroidManifest.xml" not in archive.namelist() or archive.testzip():
                    parser.error(f"Invalid APK contents in {apk}")
        except BadZipFile as error:
            parser.error(f"Invalid APK {apk}: {error}")

    # UnionPay ships its preinstalled arm64 libraries outside the APK as well.
    library_dir = apps / "UPTsmService/lib/arm64"
    libraries = sorted(library_dir.glob("*.so"))
    if not libraries:
        parser.error(f"Missing UnionPay native libraries in {library_dir}")
    files.update({f"UPTsmService/lib/arm64/{lib.name}": lib for lib in libraries})

    here = Path(__file__).resolve().parent
    template = (here.parent / "module/module.prop").read_text(encoding="utf-8")
    properties = dict(line.split("=", 1) for line in template.splitlines() if line)
    properties["name"] += " (Xiaomi 15 Ultra EEA)"
    properties["version"] += "-xuanyuan.1"
    properties["versionCode"] = str(int(properties["versionCode"]) + 1)
    properties["description"] = "为小米 15 Ultra 欧版添加国行 NFC 组件"

    with ZipFile(args.output, "w", compression=ZIP_DEFLATED, compresslevel=6) as archive:
        archive.writestr("module.prop", "".join(f"{key}={value}\n" for key, value in properties.items()))
        archive.writestr("customize.sh", (here / "customize.sh").read_text(encoding="utf-8"))
        for target, source in files.items():
            archive.write(source, f"system/product/app/{target}")


if __name__ == "__main__":
    main()
