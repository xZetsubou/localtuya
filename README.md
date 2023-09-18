![logo](https://github.com/rospogrigio/localtuya-homeassistant/blob/master/img/logo-small.png)


A Home Assistant custom Integration for local handling of Tuya-based devices.


- [Installation:](#installation)
- [Usage:](#usage)
  * [Adding the Integration](#adding-the-integration)
  * [Integration Options](#integration-options)
  * [Add Devices](#add-devices)
  * [Templates](https://github.com/xZetsubou/hass-localtuya/discussions/13)
- [Debugging](#debugging)
- [Notes](#notes)
- [Credits](#credits)

<details><summary>Supported platforms</summary>
<p>

The following Tuya device types are currently supported:
* Switches
* Lights
* Covers
* Fans
* Climates
* Vacuums

Energy monitoring (voltage, current, watts, etc.) is supported for compatible devices.

</p>
</details> 



# Installation

The easiest way and the best, Is using [HACS](https://hacs.xyz/), <br>

<details><summary>HACS installation</summary>
<p>
    
1. Open HACS and navigate to Integrations Section <br>
2. Open the Overflow Menu (⋮) in the top right corner and click on Custom repositories <br>
3. Paste `https://github.com/xZetsubou/localtuya` into the input field and select Integration from the category dropdown then click ADD. <br>
4. Now the integration should be added search in for it and install it! <br>

</p>
</details> 

<details><summary>Manual installation</summary>
<p>
    
Manual installation:
1. Download the source files from [releases](https://github.com/xZetsubou/localtuya/releases).
2. Extract/open the archive file go inside the directory `custom_components` and copy localtuya folder.
3. Paste the folder into `/config/custom_components` you can use `VSCode add-on, SMB < better or ssh` to reach /config folder

</p>
</details> 

---

# Usage:

> NOTE: You must have your Tuya device's Key and ID in order to use LocalTuya. The easiest way is to configure the Cloud API account in the integration. If you choose not to do it, there are several ways to obtain the local_keys depending on your environment and the devices you own. A good place to start getting info is https://github.com/codetheweb/tuyapi/blob/master/docs/SETUP.md  or https://pypi.org/project/tinytuya/.

> NOTE 2: If you plan to integrate these devices on a network that has internet and blocking their internet access, you must also block DNS requests (to the local DNS server, e.g. 192.168.1.1). If you only block outbound internet, then the device will sit in a zombie state; it will refuse / not respond to any connections with the localkey. Therefore, you must first connect the devices with an active internet connection, grab each device localkey, and implement the block.

## Adding the Integration
> This Integration Works without IoT Setup But It's highly recommended setup IoT Cloud To support way more features.
> 
> Features E.g.( Automatic insert needed informations to setup devices AND auto detect Sub Devices ) and more.


> Assuming you Already Installed The integration Manually or HACS
> 
#### Go to integrations page And click +Add integration bottom right and search for Local Tuya. 

#### [![Open your Home Assistant instance and show your integrations.](https://my.home-assistant.io/badges/integrations.svg)](https://my.home-assistant.io/redirect/integrations/) 

### All the bottom Information are explained here [Homeassistant Tuya](https://www.home-assistant.io/integrations/tuya/)
| Image | Details |
|----------|--------|
| ![image](https://github.com/xZetsubou/hass-localtuya/assets/46300268/d84ac9c4-b8b3-4dff-8590-91f16d0c298b) |  <h4> 1. Zone you are located in [here](https://github.com/tuya/tuya-home-assistant/blob/main/docs/regions_dataCenters.md)  <br><br><br><br> 2. ClientID [From Tuya IoT](https://www.home-assistant.io/integrations/tuya/#get-authorization-key) <br><br><br><br> 3. Secret [From Tuya IoT](https://www.home-assistant.io/integrations/tuya/#get-authorization-key) <br><br><br><br> 4-UserID From IoT [UID Pic](https://user-images.githubusercontent.com/46300268/246021288-25d56177-2cc1-45dd-adb0-458b6c5a25f3.png) <br><br><br><br> 5- Title for User Integration <br><br><br>


## Integration Options
When you add you first Hub then from LocalTuya Integration TAB click on Configure
![image](https://github.com/xZetsubou/hass-localtuya/assets/46300268/ce255b2d-8df7-43d1-a28a-186b92960174)

### You can choose action you want via the form that will show up.

## Add Devices

If you select to "Add or Edit a device", a drop-down menu will appear containing the list of detected devices (using auto-discovery if adding was selected, or the list of already configured devices if editing was selected): you can select one of these, or manually.

> **Note: The tuya app on your device must be closed for the following steps to work reliably.**


![image](https://github.com/xZetsubou/hass-localtuya/assets/46300268/e4275010-d6ba-417a-9459-586fbc3843f7)


If you have selected one entry, you only need to input the device's Friendly Name and localKey. These values will be automatically retrieved if you have configured your Cloud API account, otherwise you will need to input them manually.

Setting the scan interval is optional, it is only needed if energy/power values are not updating frequently enough by default. Values less than 10 seconds may cause stability issues.

Setting the 'Manual DPS To Add' is optional, it is only needed if the device doesn't advertise the DPS correctly until the entity has been properly initiailised. This setting can often be avoided by first connecting/initialising the device with the Tuya App, then closing the app and then adding the device in the integration. **Note: Any DPS added using this option will have a -1 value during setup.** 

Setting the 'DPIDs to send in RESET command' is optional. It is used when a device doesn't respond to any Tuya commands after a power cycle, but can be connected to (zombie state). This scenario mostly occurs when the device is blocked from accessing the internet. The DPids will vary between devices, but typically "18,19,20" is used. If the wrong entries are added here, then the device may not come out of the zombie state. Typically only sensor DPIDs entered here.

Once you press "Submit", the connection is tested to check that everything works.

![image](https://github.com/xZetsubou/hass-localtuya/assets/46300268/62a29a9a-3b3f-4852-bea8-5de69e2c4d56)



Then, it's time to add the entities: this step will take place several times. First, select the entity type from the drop-down menu to set it up.
After you have defined all the needed entities, leave the "Do not add more entities" checkbox checked: this will complete the procedure.

> Template is simply you can provide pre-config yaml devices [Guide #13](https://github.com/xZetsubou/hass-localtuya/discussions/13)

![image](https://github.com/xZetsubou/hass-localtuya/assets/46300268/1cea1b79-c0b0-41a2-bbc1-274bc5e6337c)

For each entity, the associated DP has to be selected. All the options requiring to select a DP will provide a drop-down menu showing
all the available DPs found on the device (with their current status and code if available!!) for easy identification. 

**Note: If your device requires an LocalTuya to send an initialisation value to the entity for it to work, this can be configured (in supported entities) through the 'Passive entity' option. Optionally you can specify the initialisation value to be sent**

Each entity type has different options to be configured. Here is an example for the "binary_sensor" entity:
> 0 and 1 are the values that device report it changes from devices to another

![image](https://github.com/xZetsubou/hass-localtuya/assets/46300268/ecbfc344-3280-4f7b-8df1-8cc936a917c9)

Once you configure the entities, the procedure is complete. and can access devices by click on `devices` under your Username

![image](https://github.com/xZetsubou/hass-localtuya/assets/46300268/154c94c0-d10e-485f-ac5c-c5a370b671c7)

Deleting a device simply go to device page and click on three dots next to `Download diagnostics` then delete.

<details><summary>Remap the values</summary>
<p>

Usually we use True `on` and False `off` commands for switches but if you have device that do more like single, double clicks and long press. there are 2 method to manage this devices:

#### Method 1:
add the device as select. assuming your device uses `0, 1 and 3` values then as the config would be like this:

![image](https://github.com/xZetsubou/hass-localtuya/assets/46300268/f38ae38e-3a7a-43de-ac39-7942f75db28d)

#### Method 2: Call_Service
is to add the device any way you want as sensor or switch but doing action through HA do it with call_service
to set your actions: ( The best since set any value you want ).
```yaml
service: localtuya.set_dp
data:
  device_id: 767823809c9c1f842393 # you devices_id
  dp: 1 # The DP you want to control it
  value: 0 # assuming 0 is single_click
```

</p>
</details> 


## Debugging
<details><summary>Debugging</summary>
<p>

Whenever you write a bug report, it helps tremendously if you include debug logs directly (otherwise we will just ask for them and it will take longer). So please enable debug logs like this and include them in your issue:

```yaml
logger:
  default: warning
  logs:
    custom_components.localtuya: debug
    custom_components.localtuya.pytuya: debug
```
Then, edit the device that is showing problems and check the "Enable debugging for this device" button.

</p>
</details> 

# Notes

* Do not declare anything as "tuya", such as by initiating a "switch.tuya". Using "tuya" launches Home Assistant's built-in, cloud-based Tuya integration in lieu of localtuya.

* This custom integration updates device status via pushing updates instead of polling, so status updates are fast (even when manually operated).

* The integration also supports the Tuya IoT Cloud APIs, for the retrieval of info and of the local_keys of the devices. 
The Cloud API account configuration is not mandatory (LocalTuya can work also without it) but is strongly suggested for easy retrieval (and auto-update after re-pairing a device) of local_keys. Cloud API calls are performed only at startup, and when a local_key update is needed.

<details><summary>Credits</summary>
<p>
    
# Credits:

[Rospogrigio](https://github.com/rospogrigio), The original maintainer of localtuya. this fork made when upstream version was `v5.2.1` 

[NameLessJedi](https://github.com/NameLessJedi/localtuya-homeassistant) and [mileperhour](https://github.com/mileperhour/localtuya-homeassistant) being the major sources of inspiration, and whose code for switches is substantially unchanged.

[TradeFace](https://github.com/TradeFace/tuya/), for being the only one to provide the correct code for communication with the cover (in particular, the 0x0d command for the status instead of the 0x0a, and related needs such as double reply to be received): 

sean6541, for the working (standard) Python Handler for Tuya devices.

[jasonacox](https://github.com/jasonacox), for the TinyTuya project from where I big help and refrences to upgrade integration.

[uzlonewolf](https://github.com/uzlonewolf), for maintaining in TinyTuya who improved the tool so much and introduce new features like new protocols etc..

postlund, for the ideas, for coding 95% of the refactoring and boosting the quality of this repo to levels hard to imagine (by me, at least) and teaching me A LOT of how things work in Home Assistant.

</p>
</details> 
