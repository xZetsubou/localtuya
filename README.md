![logo](https://github.com/rospogrigio/localtuya-homeassistant/blob/master/img/logo-small.png)

__A Home Assistant custom Integration for local handling of Tuya-based devices.__

## Usage and setup

<a href="https://xzetsubou.github.io/hass-localtuya/">
    <img alt="Documentation" 
        src="https://img.shields.io/website?down_message=offline&label=Documentation&up_color=007aff&up_message=online&url=https%3A%2F%2Fxzetsubou.github.io%2Fhass-localtuya%2F"
        width="190" />
</a>

<br>

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=integration&repository=hass-localtuya&owner=xZetsubou)

### Inplace replace of [official Local Tuya Integration](https://github.com/rospogrigio/localtuya)

> - [GitHub Discussion](https://github.com/xZetsubou/hass-localtuya/discussions/79)
> - [Home Assistant Community Discussion](https://community.home-assistant.io/t/local-tuya-control-tuya-devices-locally-fork-from-localtuya/634334/37?u=umu_ugg)

__Note__: Switching to this fork does not require reconfiguring everything. The existing configuration will be adopted.

1. Create a backup

2. Open this [link](https://my.home-assistant.io/redirect/hacs_repository/?category=integration&repository=hass-localtuya&owner=xZetsubou)

3. Enter your Home Assistant URL and go on

4. Add this repository

5. Remove the [official Local Tuya Integration](https://github.com/rospogrigio/localtuya) in HACS

    > It is not possible to successfully use both integrations at the same time!

    ![HACS](https://github.com/xZetsubou/hass-localtuya/blob/master/img/HACS.png)

    ![localtuya](https://github.com/xZetsubou/hass-localtuya/blob/master/img/localtuya.png)

6. Download this [(forked) Local Tuya Integration](https://github.com/xZetsubou/hass-localtuya) in HACS

    ![hass-localtuya](https://github.com/xZetsubou/hass-localtuya/blob/master/img/hass-localtuya.png)

7. Restart Home Assistant

That was all. The change should now have worked successfully and the entities should all work again.

## Features

- Supported Sub-devices - `Devices that function through gateways`
- Remote entities - `Supports IR remotes through native remote entity`
- Auto-configure devices - `Requires a cloud API setup`
- Automatic insertion - `Some fields requires a cloud API setup`
- Devices discovery - `Discovers Tuya devices on your network`
- Cloud API - `Only to help you on setup devices, can works without it.`

<br>

[Reporting an issue](https://xzetsubou.github.io/hass-localtuya/report_issue/)

<!-- ### Notes

* Do not declare anything as "tuya", such as by initiating a "switch.tuya". Using "tuya" launches Home Assistant's built-in, cloud-based Tuya integration in lieu of localtuya.

* This custom integration updates device status via pushing updates instead of polling, so status updates are fast (even when manually operated).

* The integration also supports the Tuya IoT Cloud APIs, for the retrieval of info and of the local_keys of the devices. 
The Cloud API account configuration is not mandatory (LocalTuya can work also without it) but is strongly suggested for easy retrieval (and auto-update after re-pairing a device) of local_keys. Cloud API calls are performed only at startup, and when a local_key update is needed. -->

<details><summary> Credits </summary>
<p>

[Rospogrigio](https://github.com/rospogrigio), original maintainer of LocalTuya. This fork was created when the upstream version was at `v5.2.1`.

[NameLessJedi](https://github.com/NameLessJedi/localtuya-homeassistant) and [mileperhour](https://github.com/mileperhour/localtuya-homeassistant) being the major sources of inspiration, and whose code for switches is substantially unchanged.

[TradeFace](https://github.com/TradeFace/tuya/), for being the only one to provide the correct code for communication with the cover (in particular, the 0x0d command for the status instead of the 0x0a, and related needs such as double reply to be received): 

sean6541, for the working (standard) Python Handler for Tuya devices.

[jasonacox](https://github.com/jasonacox), for the TinyTuya project from where I big help and refrences to upgrade integration.

[uzlonewolf](https://github.com/uzlonewolf), for maintaining in TinyTuya who improved the tool so much and introduce new features like new protocols etc..

postlund, for the ideas, for coding 95% of the refactoring and boosting the quality of this repo to levels hard to imagine (by me, at least) and teaching me A LOT of how things work in Home Assistant.

</p>
</details>
