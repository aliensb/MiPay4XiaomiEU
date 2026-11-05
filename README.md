# MiPay4XiaomiEU

这是一个 KernelSU 模块，用于在各种 HyperOS 修改版中安装国行 HyperOS 的 NFC 服务

也就是 门卡 交通卡 车钥匙

本模块也会恢复国行应用商店。无需商店时，可在安装前删除模块 ZIP 中的 `MIUISuperMarket` 目录。小米 15 Ultra 包使用 `system/product/app`，其他包使用 `system/app`。

Tips: 为什么要恢复国行应用商店?
- 安装"钱包"应用
- 银联组件需要更新

若您移除了应用商店, 请手工安装以上两个应用

二进制文件提取于小米完整更新包

## 支持机型

| 机型 | 代号 | 提取的固件版本 |
| --- | --- | --- |
| 小米14 | houji | OS3.0.5.0.WNCCNXM |
| 小米 15 Ultra（欧版 `OS3.0.304.0.WOAEUXM`） | xuanyuan | OS3.0.306.0.WOACNXM |
| 小米17 | pudding | OS3.0.319.0.WPCCNXM |
| 小米17 Pro | pandora | OS3.0.319.0.WBLCNXM |
| 小米17 Pro Max | popsicle | OS3.0.319.0.WPBCNXM |
| 小米17 Ultra | nezha | OS3.0.312.0.WPACNXM |

## 下载

Release 中的模块包按「提取的固件版本」命名，即 `MiPay4XiaomiEU-<固件版本>.zip`，例如：

- `MiPay4XiaomiEU-OS3.0.5.0.WNCCNXM.zip` (小米14)
- `MiPay4XiaomiEU-OS3.0.319.0.WBLCNXM.zip` (小米17 Pro)

请选择与自己 ROM 底层国行固件版本一致的包安装。小米 15 Ultra 欧版请按下节选择。

## 小米 15 Ultra 欧版安装

适配包 `MiPay4XiaomiEU-OS3.0.306.0.WOACNXM.zip` 使用国行 `OS3.0.306.0.WOACNXM` 的 NFC 组件，安装器只接受小米 15 Ultra（`xuanyuan`）欧版 `OS3.0.304.0.WOAEUXM`。该包把国行小米智能卡挂载到欧版原有的 `/product/app/MITSMClientGlobal`，避免同一个包名出现两个预装路径。

1. 在 KernelSU 中安装模块并重启。然后用 `adb shell pm path com.miui.tsmclient` 查看小米智能卡的实际 APK 路径。
2. 如果路径在 `/data/app` 下，Android 仍在使用更新版。实测更新版 `26.09.21.3.f` 会以欧版产品名 `xuanyuan_eea` 请求小米 TSM，门卡页出现 `1010004`「设备信息有误」。国行 `26.04.27.1.f` 使用机型代号 `xuanyuan`。如需回退，先确认可以接受小米智能卡本地数据被清除，已有卡片可能需要重新同步。确认后在应用管理中对「小米智能卡」选择「卸载更新」，或用已授权的 Root ADB 执行：

   ```sh
   adb shell "su -c 'pm uninstall-system-updates com.miui.tsmclient'"
   ```

3. 再次查看 APK 路径，应为 `/product/app/MITSMClientGlobal/MITSMClientGlobal.apk`。打开「钱包 → 门卡·钥匙」验证。若已是此路径，可直接打开钱包。

在 KernelSU 3.3.1 和 mountify v2.0.5 上已验证国行版能同步安全元件并加载门卡列表。首次退出页面时曾闪退一次，随后复测未重现。实体卡录入、刷卡和车钥匙配对未验证。

## 测试环境
 - 设备：小米14
 - 系统版本: OS3.0.5.0.WNCCNXM (xiaomi.eu)
 - KernelSU版本: 32179
 - KernelSU元模块: OverlayFS MetaModule
