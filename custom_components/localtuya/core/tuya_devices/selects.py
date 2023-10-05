"""
    This a file contains available tuya data
    https://developer.tuya.com/en/docs/iot/standarddescription?id=K9i5ql6waswzq
    Credits: official HA Tuya integration.
    Modified by: xZetsubou

    HOW TO ADD DEVICE: make sure the categaory doesn't exists if you want to create new category
    Define the id=DPCode_code create new code if doesn't exists,

    #TODO get values using "Get the instructions set by category"
"""

from .base import DPCode, LocalTuyaEntity, CONF_DEVICE_CLASS, EntityCategory

# from const.py this is temporarily.

from ...select import CONF_OPTIONS as OPS_VALS
from ...select import CONF_OPTIONS_FRIENDLY as OPS_NAME


def localtuya_selector(options, options_name=None):
    """Generate localtuya select configs"""
    data = {OPS_VALS: options, OPS_NAME: options_name}
    return data


# Select Options [ options : friendly name for options ]
MORING_NIGHT = {OPS_VALS: "morning,night", OPS_NAME: "Morning,Night"}

# Cover
FORWARD_BACK = {OPS_VALS: "forward,back", OPS_NAME: "Forward,Back"}
FAN_WORK_MODE = {OPS_VALS: "contiuation,point", OPS_NAME: "Auto,Manual"}


# THIS IS FOR alarm_control_panel.py
# Multi-functional Sensor
MASTER_MODE = {OPS_VALS: "disarmed,arm,home,sos", OPS_NAME: "Disarmed,Arm,Home,sos"}
ALARM_VOLUME = {OPS_VALS: "low,middle,high,mute", OPS_NAME: "Low,Middle,High,Mute"}
ALARM_RINGTONE = {OPS_VALS: "1,2,3,4,5", OPS_NAME: "1,2,3,4,5"}
ALARM_STATES = {
    OPS_VALS: "alarm_sound,alarm_light,alarm_sound_light,normal",
    OPS_NAME: "Sound,Light,Sound and Light,Normal",
}

# Coffee maker
CUP_NUMBER = {
    OPS_VALS: "1,2,3,4,5,6,7,8,9,10,11,12",
    OPS_NAME: "1,2,3,4,5,6,7,8,9,10,11,12",
}
CONCENTRATION_SET = {OPS_VALS: "regular,middle,bold", OPS_NAME: "Regular,Middle,Bold"}
MATERIAL = {OPS_VALS: "bean,powder", OPS_NAME: "Bean,Powder"}
COFFE_MODES = {
    OPS_VALS: "espresso,americano,machiatto,caffe_latte,cafe_mocha,cappuccino",
    OPS_NAME: "Espresso,Americano,Machiatto,Caffe Latte,Cafe Mocha,Cappuccino",
}

# Switch alikes
RELAY_STATUS = {OPS_VALS: "power_on,power_off,last", OPS_NAME: "ON,OFF,Last State"}
RELAY_STATUS_V2 = {OPS_VALS: "0,1,2", OPS_NAME: "ON,OFF,Last State"}
DIMMER_RELAY_STATUS = {OPS_VALS: "on,off,memory", OPS_NAME: "ON,OFF,Last State"}

LED_TYPE_1 = {
    OPS_VALS: "led,incandescent,halogen",
    OPS_NAME: "LED,Incandescence,Halogen",
}
LIGHT_MODE = {OPS_VALS: "relay,pos,none", OPS_NAME: "State,Position,OFF"}

# Heater
HEATER_MODES = {OPS_VALS: "smart,auto", OPS_NAME: "Smart,Auto"}
HEATER_LEVELS = {OPS_VALS: "1,2,3", OPS_NAME: "1,2,3"}

COUNTDOWN = {OPS_VALS: "cancel,1,2,3,4,5,6", OPS_NAME: "Cancel,1H,2H,3H,4H,5H,6H"}
COUNTDOWN_SET = {
    OPS_VALS: "cancel,1h,2h,3h,4h,5h,6h",
    OPS_NAME: "Cancel,1H,2H,3H,4H,5H,6H",
}

# Siren Alarm
BRIGHT_STATE = {OPS_VALS: "low,middle,high,strong", OPS_NAME: "Low,Middle,High,Strong"}

# Smart Camera
IPC_WORK_MODE = {OPS_VALS: "0,1", OPS_NAME: "Low Power,Continuous"}
DECIBEL_SENSITIVITY = {OPS_VALS: "0,1", OPS_NAME: "Low Sensitivity,Hight Sensitivity"}
IPC_WORK_MODE = {OPS_VALS: "0,1", OPS_NAME: "Low Power,Continuous"}
RECORD_MODE = {OPS_VALS: "1,2", OPS_NAME: "Record Events Only,Allways Record"}
FLIGHT_BRIGHT_MODE = {OPS_VALS: "0,1", OPS_NAME: "Manual,Auto"}
PIR_SENSITIVITY = {OPS_VALS: "0,1,2", OPS_NAME: "Low,Medium,High"}
BASIC_NIGHTVISION = {OPS_VALS: "0,1,2", OPS_NAME: "Auto,OFF,ON"}
BASIC_ANTI_FLICKER = {OPS_VALS: "0,1,2", OPS_NAME: "Disable,50 Hz,60 Hz"}
MOTION_SENSITIVITY = {OPS_VALS: "0,1,2", OPS_NAME: "Low,Medium,High"}
PTZ_CONTROL = {
    OPS_VALS: "0,1,2,3,4,5,6,7",
    OPS_NAME: "UP,Upper Right,Right,Bottom Right,Down,Bottom Left,Left,Upper Left",
}

# Fingerbot
CLICK_SWITCH_TOGGLE = {OPS_VALS: "click,switch,toggle", OPS_NAME: "Click,Switch,Toggle"}

# VACCUM
VACCUM_MODE = {
    OPS_VALS: "standby,random,smart,wall_follow,mop,spiral,left_spiral,right_spiral,right_bow,left_bow,partial_bow,chargego",
    OPS_NAME: "StandBy,Random,Smart,Edges,Mop,Spiral,Left Spiral,Right Spiral,Right Bow,Left Bow,Partial Bow,Recharge",
}
VACCUM_CISTERN = {
    OPS_VALS: "low,middle,high,closed",
    OPS_NAME: "Low,Middle,High,Closed",
}
VACCUM_COLLECTION_MODE = {
    OPS_VALS: "small,middle,large",
    OPS_NAME: "Small,Middle,Large",
}

# FAN
SWING_30_60_90 = {OPS_VALS: "30,60,90", OPS_NAME: "30 Deg,60 Deg,90 Deg"}
FAN_LIGHT_MODE = {
    OPS_VALS: "white,colour,colourful",
    OPS_NAME: "White,Colour,Colourful",
}

# Humidifier
MOODLIGHTING = {OPS_VALS: "1,2,3,4,5", OPS_NAME: "1,2,3,4,5"}
HUMIDIFER_LEVEL = {
    OPS_VALS: "level_1,level_2,level_3,level_4,level_5,level_6,level_7,level_8,level_9,level_10",
    OPS_NAME: "Level 1,Level 2,Level 3,Level 4,Level 5,Level 6,Level 7,Level 8,Level 9,Level 10",
}
SPRAY_MODE = {
    OPS_VALS: "auto,health,baby,sleep,humidity,work",
    OPS_NAME: "Auto,Health,Baby,Sleep,Humidity,Work",
}

# Dehumidifier
DEHUMIDITY_SET_ENUM = {OPS_VALS: "10,20,30,40,50", OPS_NAME: "10,20,30,40,50"}

SELECTS: dict[str, tuple[LocalTuyaEntity, ...]] = {
    # Multi-functional Sensor
    # https://developer.tuya.com/en/docs/iot/categorydgnbj?id=Kaiuz3yorvzg3
    "dgnbj": (
        LocalTuyaEntity(
            id=DPCode.ALARM_VOLUME,
            name="volume",
            entity_category=EntityCategory.CONFIG,
            custom_configs=ALARM_VOLUME,
        ),
        LocalTuyaEntity(
            id=DPCode.ALARM_RINGTONE,
            name="Ringtone",
            entity_category=EntityCategory.CONFIG,
            custom_configs=ALARM_RINGTONE,
        ),
    ),
    # Heater
    "kt": (
        LocalTuyaEntity(
            id=(DPCode.C_F, DPCode.TEMP_UNIT_CONVERT),
            name="Temperature Unit",
            custom_configs=localtuya_selector("c,f", "Celsius,Fahrenheit"),
        ),
    ),
    # Heater
    "rs": (
        LocalTuyaEntity(
            id=(DPCode.C_F, DPCode.TEMP_UNIT_CONVERT),
            name="Temperature Unit",
            custom_configs=localtuya_selector("c,f", "Celsius,Fahrenheit"),
        ),
        LocalTuyaEntity(
            id=DPCode.CRUISE_MODE,
            name="Cruise mode",
            custom_configs=localtuya_selector(
                "all_day,water_control,single_cruise", "Always,Water,Once"
            ),
        ),
    ),
    # Coffee maker
    # https://developer.tuya.com/en/docs/iot/categorykfj?id=Kaiuz2p12pc7f
    "kfj": (
        LocalTuyaEntity(
            id=DPCode.CUP_NUMBER,
            name="Cups",
            icon="mdi:numeric",
            custom_configs=CUP_NUMBER,
        ),
        LocalTuyaEntity(
            id=DPCode.CONCENTRATION_SET,
            name="Concentration",
            icon="mdi:altimeter",
            entity_category=EntityCategory.CONFIG,
            custom_configs=CONCENTRATION_SET,
        ),
        LocalTuyaEntity(
            id=DPCode.MATERIAL,
            name="Material",
            entity_category=EntityCategory.CONFIG,
            custom_configs=MATERIAL,
        ),
        LocalTuyaEntity(
            id=DPCode.MODE,
            name="Mode",
            icon="mdi:coffee",
            custom_configs=COFFE_MODES,
        ),
    ),
    # Switch
    # https://developer.tuya.com/en/docs/iot/s?id=K9gf7o5prgf7s
    "kg": (
        LocalTuyaEntity(
            id=DPCode.RELAY_STATUS,
            icon="mdi:circle-double",
            entity_category=EntityCategory.CONFIG,
            name="Relay Status",
            custom_configs=RELAY_STATUS,
            condition_contains_any=RELAY_STATUS[OPS_VALS].split(","),
        ),
        LocalTuyaEntity(
            id=DPCode.RELAY_STATUS,
            icon="mdi:circle-double",
            entity_category=EntityCategory.CONFIG,
            name="Relay Status",
            custom_configs=RELAY_STATUS_V2,
        ),
        LocalTuyaEntity(
            id=DPCode.LIGHT_MODE,
            entity_category=EntityCategory.CONFIG,
            custom_configs=LIGHT_MODE,
            name="Light Mode",
        ),
    ),
    # Heater
    # https://developer.tuya.com/en/docs/iot/categoryqn?id=Kaiuz18kih0sm
    "qn": (
        LocalTuyaEntity(
            id=DPCode.MODE,
            name="Mode",
            custom_configs=HEATER_MODES,
        ),
        LocalTuyaEntity(
            id=DPCode.LEVEL,
            name="Temperature Level",
            icon="mdi:thermometer-lines",
            custom_configs=HEATER_LEVELS,
        ),
        LocalTuyaEntity(
            id=DPCode.COUNTDOWN,
            name="Set Countdown",
            icon="mdi:timer-cog-outline",
            custom_configs=COUNTDOWN,
        ),
        LocalTuyaEntity(
            id=DPCode.COUNTDOWN_SET,
            name="Set Countdown",
            icon="mdi:timer-cog-outline",
            custom_configs=COUNTDOWN_SET,
        ),
        LocalTuyaEntity(
            id=(DPCode.C_F, DPCode.TEMP_UNIT_CONVERT),
            name="Temperature Unit",
            custom_configs=localtuya_selector("c,f", "Celsius,Fahrenheit"),
        ),
    ),
    # Siren Alarm
    # https://developer.tuya.com/en/docs/iot/categorysgbj?id=Kaiuz37tlpbnu
    "sgbj": (
        LocalTuyaEntity(
            id=DPCode.ALARM_VOLUME,
            name="Volume",
            entity_category=EntityCategory.CONFIG,
            custom_configs=ALARM_VOLUME,
        ),
        LocalTuyaEntity(
            id=DPCode.ALARM_STATE,
            name="State",
            entity_category=EntityCategory.CONFIG,
            custom_configs=ALARM_STATES,
        ),
        LocalTuyaEntity(
            id=DPCode.BRIGHT_STATE,
            name="Brightness",
            entity_category=EntityCategory.CONFIG,
            custom_configs=BRIGHT_STATE,
        ),
    ),
    # Smart Camera
    # https://developer.tuya.com/en/docs/iot/categorysp?id=Kaiuz35leyo12
    "sp": (
        LocalTuyaEntity(
            id=DPCode.IPC_WORK_MODE,
            entity_category=EntityCategory.CONFIG,
            name="Working mode",
            custom_configs=IPC_WORK_MODE,
        ),
        LocalTuyaEntity(
            id=DPCode.DECIBEL_SENSITIVITY,
            icon="mdi:volume-vibrate",
            entity_category=EntityCategory.CONFIG,
            name="Decibel Sensitivity",
            custom_configs=DECIBEL_SENSITIVITY,
        ),
        LocalTuyaEntity(
            id=DPCode.RECORD_MODE,
            icon="mdi:record-rec",
            entity_category=EntityCategory.CONFIG,
            name="Record Mode",
            custom_configs=RECORD_MODE,
        ),
        LocalTuyaEntity(
            id=DPCode.BASIC_NIGHTVISION,
            icon="mdi:theme-light-dark",
            entity_category=EntityCategory.CONFIG,
            name="IR Night Vision",
            custom_configs=BASIC_NIGHTVISION,
        ),
        LocalTuyaEntity(
            id=DPCode.BASIC_ANTI_FLICKER,
            icon="mdi:image-outline",
            entity_category=EntityCategory.CONFIG,
            name="Anti-Flicker",
            custom_configs=BASIC_ANTI_FLICKER,
        ),
        LocalTuyaEntity(
            id=DPCode.MOTION_SENSITIVITY,
            icon="mdi:motion-sensor",
            entity_category=EntityCategory.CONFIG,
            name="Motion Sensitivity",
            custom_configs=MOTION_SENSITIVITY,
        ),
        LocalTuyaEntity(
            id=DPCode.PTZ_CONTROL,
            icon="mdi:image-filter-tilt-shift",
            entity_category=EntityCategory.CONFIG,
            name="PTZ control",
            custom_configs=PTZ_CONTROL,
        ),
        LocalTuyaEntity(
            id=DPCode.FLIGHT_BRIGHT_MODE,
            entity_category=EntityCategory.CONFIG,
            name="Brightness mode",
            custom_configs=FLIGHT_BRIGHT_MODE,
        ),
        LocalTuyaEntity(
            id=DPCode.PIR_SENSITIVITY,
            entity_category=EntityCategory.CONFIG,
            name="PIR sensitivity",
            custom_configs=PIR_SENSITIVITY,
        ),
    ),
    # Dimmer Switch
    # https://developer.tuya.com/en/docs/iot/categorytgkg?id=Kaiuz0ktx7m0o
    "tgkg": (
        LocalTuyaEntity(
            id=DPCode.RELAY_STATUS,
            icon="mdi:circle-double",
            entity_category=EntityCategory.CONFIG,
            name="Relay Status",
            custom_configs=DIMMER_RELAY_STATUS,
            condition_contains_any=DIMMER_RELAY_STATUS[OPS_VALS].split(","),
        ),
        LocalTuyaEntity(
            id=DPCode.RELAY_STATUS,
            icon="mdi:circle-double",
            entity_category=EntityCategory.CONFIG,
            name="Relay Status",
            custom_configs=RELAY_STATUS_V2,
        ),
        LocalTuyaEntity(
            id=DPCode.LIGHT_MODE,
            entity_category=EntityCategory.CONFIG,
            name="Light Mode",
            custom_configs=LIGHT_MODE,
        ),
        LocalTuyaEntity(
            id=DPCode.LED_TYPE_1,
            entity_category=EntityCategory.CONFIG,
            name="Led Type 1",
            custom_configs=LED_TYPE_1,
        ),
        LocalTuyaEntity(
            id=DPCode.LED_TYPE_2,
            entity_category=EntityCategory.CONFIG,
            name="Led Type 2",
            custom_configs=LED_TYPE_1,
        ),
        LocalTuyaEntity(
            id=DPCode.LED_TYPE_3,
            entity_category=EntityCategory.CONFIG,
            name="Led Type 3",
            custom_configs=LED_TYPE_1,
        ),
    ),
    # Dimmer
    # https://developer.tuya.com/en/docs/iot/tgq?id=Kaof8ke9il4k4
    "tgq": (
        LocalTuyaEntity(
            id=DPCode.LED_TYPE_1,
            entity_category=EntityCategory.CONFIG,
            name="Led Type 1",
            custom_configs=LED_TYPE_1,
        ),
        LocalTuyaEntity(
            id=DPCode.LED_TYPE_2,
            entity_category=EntityCategory.CONFIG,
            name="Led Type 2",
            custom_configs=LED_TYPE_1,
        ),
    ),
    # Fingerbot
    "szjqr": (
        LocalTuyaEntity(
            id=DPCode.MODE,
            entity_category=EntityCategory.CONFIG,
            name="Fingerbot Mode",
            custom_configs=CLICK_SWITCH_TOGGLE,
        ),
    ),
    # Robot Vacuum
    # https://developer.tuya.com/en/docs/iot/fsd?id=K9gf487ck1tlo
    "sd": (
        LocalTuyaEntity(
            id=DPCode.CISTERN,
            entity_category=EntityCategory.CONFIG,
            icon="mdi:water-opacity",
            name="Water Tank Adjustment",
            custom_configs=VACCUM_CISTERN,
        ),
        LocalTuyaEntity(
            id=DPCode.COLLECTION_MODE,
            entity_category=EntityCategory.CONFIG,
            icon="mdi:air-filter",
            name="Dust Collection Mode",
            custom_configs=VACCUM_COLLECTION_MODE,
        ),
        LocalTuyaEntity(
            id=DPCode.MODE,
            entity_category=EntityCategory.CONFIG,
            icon="mdi:layers-outline",
            name="Mode",
            custom_configs=VACCUM_MODE,
        ),
    ),
    # Fan
    # https://developer.tuya.com/en/docs/iot/f?id=K9gf45vs7vkge
    "fs": (
        LocalTuyaEntity(
            id=DPCode.FAN_VERTICAL,
            entity_category=EntityCategory.CONFIG,
            icon="mdi:format-vertical-align-center",
            name="Vertical swing",
            custom_configs=SWING_30_60_90,
        ),
        LocalTuyaEntity(
            id=DPCode.FAN_HORIZONTAL,
            entity_category=EntityCategory.CONFIG,
            icon="mdi:format-horizontal-align-center",
            name="Horizontal swing",
            custom_configs=SWING_30_60_90,
        ),
        LocalTuyaEntity(
            id=DPCode.WORK_MODE,
            entity_category=EntityCategory.CONFIG,
            icon="mdi:ceiling-fan-light",
            name="Light mode",
            custom_configs=FAN_LIGHT_MODE,
        ),
        LocalTuyaEntity(
            id=DPCode.COUNTDOWN,
            entity_category=EntityCategory.CONFIG,
            icon="mdi:timer-cog-outline",
            name="Countdown",
            custom_configs=COUNTDOWN,
        ),
        LocalTuyaEntity(
            id=DPCode.COUNTDOWN_SET,
            entity_category=EntityCategory.CONFIG,
            icon="mdi:timer-cog-outline",
            name="Countdown",
            custom_configs=COUNTDOWN_SET,
        ),
    ),
    # Curtain
    # https://developer.tuya.com/en/docs/iot/f?id=K9gf46o5mtfyc
    "cl": (
        LocalTuyaEntity(
            id=(DPCode.CONTROL_BACK_MODE, DPCode.CONTROL_BACK),
            name="Motor Direction",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:swap-vertical",
            custom_configs=FORWARD_BACK,
        ),
        LocalTuyaEntity(
            id=DPCode.MOTOR_MODE,
            name="Motor Mode",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:cog-transfer",
            custom_configs=FAN_WORK_MODE,
        ),
        LocalTuyaEntity(
            id=DPCode.MODE,
            entity_category=EntityCategory.CONFIG,
            name="Cover Mode",
            custom_configs=MORING_NIGHT,
        ),
    ),
    # Humidifier
    # https://developer.tuya.com/en/docs/iot/categoryjsq?id=Kaiuz1smr440b
    "jsq": (
        LocalTuyaEntity(
            id=DPCode.SPRAY_MODE,
            entity_category=EntityCategory.CONFIG,
            icon="mdi:spray",
            name="Spraying mode",
            custom_configs=SPRAY_MODE,
        ),
        LocalTuyaEntity(
            id=DPCode.LEVEL,
            entity_category=EntityCategory.CONFIG,
            icon="mdi:spray",
            name="Spraying level",
            custom_configs=HUMIDIFER_LEVEL,
        ),
        LocalTuyaEntity(
            id=DPCode.MOODLIGHTING,
            entity_category=EntityCategory.CONFIG,
            icon="mdi:lightbulb-multiple",
            name="Mood light",
            custom_configs=MOODLIGHTING,
        ),
        LocalTuyaEntity(
            id=DPCode.COUNTDOWN,
            entity_category=EntityCategory.CONFIG,
            icon="mdi:timer-cog-outline",
            name="Countdown",
            custom_configs=COUNTDOWN,
        ),
        LocalTuyaEntity(
            id=DPCode.COUNTDOWN_SET,
            entity_category=EntityCategory.CONFIG,
            icon="mdi:timer-cog-outline",
            name="Countdown",
            custom_configs=COUNTDOWN_SET,
        ),
    ),
    # Air Purifier
    # https://developer.tuya.com/en/docs/iot/f?id=K9gf46h2s6dzm
    "kj": (
        LocalTuyaEntity(
            id=DPCode.COUNTDOWN,
            entity_category=EntityCategory.CONFIG,
            icon="mdi:timer-cog-outline",
            name="Countdown",
            custom_configs=COUNTDOWN,
        ),
        LocalTuyaEntity(
            id=DPCode.COUNTDOWN_SET,
            entity_category=EntityCategory.CONFIG,
            icon="mdi:timer-cog-outline",
            name="Countdown",
            custom_configs=COUNTDOWN_SET,
        ),
    ),
    # Dehumidifier
    # https://developer.tuya.com/en/docs/iot/categorycs?id=Kaiuz1vcz4dha
    "cs": (
        LocalTuyaEntity(
            id=DPCode.COUNTDOWN_SET,
            entity_category=EntityCategory.CONFIG,
            icon="mdi:timer-cog-outline",
            name="Countdown",
            custom_configs=COUNTDOWN,
        ),
        LocalTuyaEntity(
            id=DPCode.DEHUMIDITY_SET_ENUM,
            name="Target Humidity",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:water-percent",
            custom_configs=DEHUMIDITY_SET_ENUM,
        ),
    ),
    # sous vide cookers
    # https://developer.tuya.com/en/docs/iot/f?id=K9r2v9hgmyk3h
    "mzj": (
        LocalTuyaEntity(
            id=DPCode.MODE,
            entity_category=EntityCategory.CONFIG,
            name="Cooking Mode",
            custom_configs=localtuya_selector(
                "vegetables,meat,shrimp,fish,chicken,drumsticks,beef,rice",
                "Vegetables,Meat,Shrimp,Fish,Chicken,Drumsticks,Beef,Rice",
            ),
        ),
    ),
    "wk": (
        LocalTuyaEntity(
            id=DPCode.SENSORTYPE,
            entity_category=EntityCategory.CONFIG,
            name="Temperature sensor",
            custom_configs=localtuya_selector("0,1,2", "Internal;External;Both"),
        ),
    ),
}

# Socket (duplicate of `kg`)
# https://developer.tuya.com/en/docs/iot/s?id=K9gf7o5prgf7s
SELECTS["cz"] = SELECTS["kg"]

# Power Socket (duplicate of `kg`)
# https://developer.tuya.com/en/docs/iot/s?id=K9gf7o5prgf7s
SELECTS["pc"] = SELECTS["kg"]

SELECTS["tdq"] = SELECTS["kg"]

# Heater
SELECTS["rs"] = SELECTS["kt"]
