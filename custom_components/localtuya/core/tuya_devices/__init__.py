"""
    Tuya Devices: https://xzetsubou.github.io/hass-localtuya/auto_configure/

    This functionality is similar to HA Tuya, as it retrieves the category and searches for the corresponding categories. 
    The categories data has been improved & modified to work seamlessly with localtuya

    Device Data: You can obtain all the data for your device from Home Assistant by directly downloading the diagnostics or using entry diagnostics.
        Alternative: Use Tuya IoT.

    Add a new device or modify an existing one:
        1. Make sure the device category doesn't already exist. If you are creating a new one, you can modify existing categories.
        2. In order to add a device, you need to specify the category of the device you want to add inside the entity type dictionary.
    
    Add entities to devices:
        1. Open the file with the name of the entity type on which you want to make changes [e.g. switches.py] and search for your device category.
        2. You can add entities inside the tuple value of the dictionary by including LocalTuyaEntity and passing the parameters for the entity configurations.
        3. These configurations include "id" (required), "icon" (optional), "device_class" (optional), "state_class" (optional), and "name" (optional) [Using COVERS as an example]
            Example: "3 ( code: percent_state , value: 0 )" - Refer to the Device Data section above for more details.
                current_state_dp = DPCode.PERCENT_STATE < This maps the "percent_state" code DP to the current_state_dp configuration.

            If the configuration is not DPS, it will be inserted through "custom_configs". This is used to inject any configuration into the entity configuration
                Example: custom_configs={"positioning_mode": "position"}. I hope that clarifies the concept
        Check for more details at the URL above
"""


from .base import LocalTuyaEntity, CONF_DPS_STRINGS
from enum import Enum
from homeassistant.const import Platform, CONF_FRIENDLY_NAME, CONF_PLATFORM, CONF_ID

import logging

# Supported files
from .alarm_control_panels import ALARMS  # not added yet
from .binary_sensors import BINARY_SENSORS
from .buttons import BUTTONS
from .climates import CLIMATES
from .covers import COVERS
from .fans import FANS
from .humidifiers import HUMIDIFIERS
from .lights import LIGHTS
from .numbers import NUMBERS
from .selects import SELECTS
from .sensors import SENSORS
from .sirens import SIRENS
from .switches import SWITCHES
from .vacuums import VACUUMS

# The supported PLATFORMS [ Platform: Data ]
DATA_PLATFORMS = {
    # Platform.ALARM_CONTROL_PANEL: ALARMS,
    Platform.BINARY_SENSOR: BINARY_SENSORS,
    Platform.BUTTON: BUTTONS,
    Platform.CLIMATE: CLIMATES,
    Platform.COVER: COVERS,
    Platform.FAN: FANS,
    Platform.HUMIDIFIER: HUMIDIFIERS,
    Platform.LIGHT: LIGHTS,
    Platform.NUMBER: NUMBERS,
    Platform.SELECT: SELECTS,
    Platform.SENSOR: SENSORS,
    Platform.SIREN: SIRENS,
    Platform.SWITCH: SWITCHES,
    Platform.VACUUM: VACUUMS,
}

_LOGGER = logging.getLogger(__name__)


def gen_localtuya_entities(localtuya_data: dict, tuya_category: str) -> list[dict]:
    """Return localtuya entities using the data that provided from TUYA"""
    detected_dps: list = localtuya_data.get(CONF_DPS_STRINGS)
    device_name: str = localtuya_data.get(CONF_FRIENDLY_NAME).strip()
    device_cloud_data: dict = localtuya_data.get("device_cloud_data", {})
    dps_data = device_cloud_data.get("dps_data", {})

    if not tuya_category or not detected_dps:
        return

    entities = {}

    for platform, tuya_data in DATA_PLATFORMS.items():
        if cat_data := tuya_data.get(tuya_category):
            for ent_data in cat_data:
                main_confs = ent_data.data
                localtuya_conf = ent_data.localtuya_conf
                # Conditions
                contains_any: list[str] = ent_data.contains_any
                local_entity = {}

                # used_dp = 0
                for k, code in localtuya_conf.items():
                    if type(code) == Enum:
                        code = code.value

                    if isinstance(code, tuple):
                        for dp_code in code:
                            if any(dp_code in dps.split() for dps in detected_dps):
                                code = parse_enum(dp_code)
                                break
                            else:
                                code = None

                    for dp_data in detected_dps:
                        dp_data: str = dp_data.lower()

                        if contains_any is not None:
                            if not any(cond in dp_data for cond in contains_any):
                                continue

                        if code and code.lower() in dp_data.split():
                            # Same method we use in config_flow to get dp.
                            local_entity[k] = dp_data.split(" ")[0]

                        # used_dp += 1
                if local_entity:
                    # Entity most contains ID
                    if not local_entity.get(CONF_ID):
                        continue
                    # Workaround to Prevent duplicated id.
                    if local_entity[CONF_ID] in entities:
                        continue

                    # Prevent duplicated friendly_name e.g. [switch_switch]
                    # if name := main_confs.get(CONF_FRIENDLY_NAME):
                    #     if name.split()[0].lower() in device_name.split()[-1].lower():
                    #         main_confs[CONF_FRIENDLY_NAME] = ""

                    local_entity.update(main_confs)
                    local_entity[CONF_PLATFORM] = platform
                    entities[local_entity.get(CONF_ID)] = local_entity

    # sort entites by id
    sorted_ids = sorted(entities, key=int)

    # convert to list of configs
    list_entities = [entities.get(id) for id in sorted_ids]

    # return []
    return list_entities


def parse_enum(dp_code):
    """get enum value if code type is enum"""
    try:
        parsed_dp_code = dp_code.value
    except:
        parsed_dp_code = dp_code

    return parsed_dp_code


def get_dp_value(dp, dps_data):
    ...
