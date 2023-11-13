# Overview
LocalTuya is an [HomeAssistant](https://www.home-assistant.io/) integration that enables you to control your Tuya-based smart devices directly within your local network. 

!!! info "LocalTuya as a Hub"
    `LocalTuya` serves as a hub. After setup, whether using `cloud` or `no cloud`, you can manage your devices via the entry configuration UI by clicking on `configure` (1).
    { .annotate }

    1. ![](images/configure.png)
 
!!! info "Cloud API"
    LocalTuya uses the cloud solely to obtain device data and pre-fill the required fields for you.

    It offers numerous features to simplify device setup.

    `LocalTuya` can be used independently of the cloud.

[:simple-homeassistantcommunitystore: Add repository to HACS](https://my.home-assistant.io/redirect/hacs_repository/?category=integration&repository=hass-localtuya&owner=xZetsubou){ target=_blank .md-button }

## Features
- [Cloud API](/cloud_api) 
- Supported protocols: `3.1`, `3.2`, `3.3`, `3.4`, and `3.5`
- Auto-configure devices - *`Requires a cloud API setup`*
- Automatic insertion - *`Requires a cloud API setup`*
- Devices discovery - *`Discovers Tuya devices on your network`* 

## Supported Platforms
- Binary Sensor
- Button
- Climate
- Cover
- Fan
- Humidifier
- Light
- Number
- Selector
- Sensor
- Siren
- Switch
- Vacuum
