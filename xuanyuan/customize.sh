# This package was assembled for the EEA build on the target Xiaomi 15 Ultra.
[ "$(getprop ro.product.device)" = xuanyuan ] || abort "This module requires Xiaomi 15 Ultra (xuanyuan)."
[ "$(getprop ro.product.build.version.incremental)" = OS3.0.304.0.WOAEUXM ] ||
  abort "This module requires HyperOS OS3.0.304.0.WOAEUXM."
[ -d /product/app/MITSMClientGlobal ] || abort "The EEA TSM system app was not found."

ui_print "- Xiaomi 15 Ultra: EEA OS3.0.304.0.WOAEUXM"
ui_print "- NFC components: CN OS3.0.306.0.WOACNXM"

if [ "$BOOTMODE" = true ]; then
  case "$(pm path com.miui.tsmclient 2>/dev/null)" in
    package:/data/app/*)
      ui_print "! 检测到小米智能卡的更新版。重启后请参照 README 卸载该应用的更新，启用国行版。"
      ui_print "! 回退会清除小米智能卡的本地数据，请确认后手动操作。"
      ;;
  esac
fi
