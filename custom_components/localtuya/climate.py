"""Platform to locally control Tuya-based climate devices.
    # PRESETS and HVAC_MODE Needs to be handle in better way.
"""

import re
import asyncio
import logging
from functools import partial
from .config_flow import _col_to_select
from homeassistant.helpers import selector

import voluptuous as vol
from homeassistant.components.climate import (
    DEFAULT_MAX_TEMP,
    DEFAULT_MIN_TEMP,
    DOMAIN,
    ClimateEntity,
)
from homeassistant.components.climate.const import (
    HVACMode,
    HVACAction,
    PRESET_AWAY,
    PRESET_ECO,
    PRESET_HOME,
    PRESET_NONE,
    ClimateEntityFeature,
)
from homeassistant.const import (
    ATTR_TEMPERATURE,
    CONF_TEMPERATURE_UNIT,
    PRECISION_HALVES,
    PRECISION_TENTHS,
    PRECISION_WHOLE,
    UnitOfTemperature,
)
from homeassistant.util.unit_system import US_CUSTOMARY_SYSTEM
from .entity import LocalTuyaEntity, async_setup_entry
from .const import (
    CONF_CURRENT_TEMPERATURE_DP,
    CONF_ECO_DP,
    CONF_ECO_VALUE,
    CONF_HEURISTIC_ACTION,
    CONF_HVAC_ACTION_DP,
    CONF_HVAC_ACTION_SET,
    CONF_HVAC_MODE_DP,
    CONF_HVAC_MODE_SET,
    CONF_PRECISION,
    CONF_PRESET_DP,
    CONF_PRESET_SET,
    CONF_TARGET_PRECISION,
    CONF_TARGET_TEMPERATURE_DP,
    CONF_TEMPERATURE_STEP,
    CONF_MIN_TEMP,
    CONF_MAX_TEMP,
    CONF_HVAC_ADD_OFF,
    CONF_FAN_SPEED_DP,
    CONF_FAN_SPEED_LIST,
)

_LOGGER = logging.getLogger(__name__)


HVAC_OFF = {HVACMode.OFF.value: "off"}
RENAME_HVAC_MODE_SETS = {  # Migrate to 3
    ("manual", "Manual", "hot", "m", "True"): HVACMode.HEAT.value,
    ("auto", "0", "p", "Program"): HVACMode.AUTO.value,
    ("freeze", "cold", "1"): HVACMode.COOL.value,
    ("wet"): HVACMode.DRY.value,
}
RENAME_ACTION_SETS = {  # Migrate to 3
    ("open", "opened", "heating", "Heat", "True"): HVACAction.HEATING.value,
    ("closed", "close", "no_heating"): HVACAction.IDLE.value,
    ("Warming", "warming", "False"): HVACAction.IDLE.value,
    ("cooling"): HVACAction.COOLING.value,
    ("off"): HVACAction.OFF.value,
}
RENAME_PRESET_SETS = {
    "Holiday": (PRESET_AWAY),
    "Program": (PRESET_HOME),
    "Manual": (PRESET_NONE, "manual"),
    "Auto": "auto",
    "Manual": "manual",
    "Smart": "smart",
    "Comfort": "comfortable",
    "ECO": "eco",
}


HVAC_MODE_SETS = {
    HVACMode.OFF: False,
    HVACMode.AUTO: "auto",
    HVACMode.COOL: "cold",
    HVACMode.HEAT: "warm",
    HVACMode.DRY: "dehumidify",
    HVACMode.FAN_ONLY: "air",
}

HVAC_ACTION_SETS = {
    HVACAction.HEATING: "opened",
    HVACAction.IDLE: "closed",
}


TEMPERATURE_CELSIUS = "celsius"
TEMPERATURE_FAHRENHEIT = "fahrenheit"
DEFAULT_TEMPERATURE_UNIT = TEMPERATURE_CELSIUS
DEFAULT_PRECISION = 0.1
DEFAULT_TEMPERATURE_STEP = PRECISION_HALVES
# Empirically tested to work for AVATTO thermostat
MODE_WAIT = 0.1

FAN_SPEEDS_DEFAULT = "auto,low,middle,high"


def flow_schema(dps):
    """Return schema used in config flow."""
    return {
        vol.Optional(CONF_TARGET_TEMPERATURE_DP): _col_to_select(dps, is_dps=True),
        vol.Optional(CONF_CURRENT_TEMPERATURE_DP): _col_to_select(dps, is_dps=True),
        vol.Optional(CONF_TEMPERATURE_STEP): _col_to_select(
            [PRECISION_WHOLE, PRECISION_HALVES, PRECISION_TENTHS]
        ),
        vol.Optional(CONF_MIN_TEMP, default=DEFAULT_MIN_TEMP): vol.Coerce(float),
        vol.Optional(CONF_MAX_TEMP, default=DEFAULT_MAX_TEMP): vol.Coerce(float),
        vol.Optional(CONF_PRECISION, default=str(DEFAULT_PRECISION)): _col_to_select(
            [PRECISION_WHOLE, PRECISION_HALVES, PRECISION_TENTHS]
        ),
        vol.Optional(
            CONF_TARGET_PRECISION, default=str(DEFAULT_PRECISION)
        ): _col_to_select([PRECISION_WHOLE, PRECISION_HALVES, PRECISION_TENTHS]),
        vol.Optional(CONF_HVAC_MODE_DP): _col_to_select(dps, is_dps=True),
        vol.Optional(
            CONF_HVAC_MODE_SET, default=HVAC_MODE_SETS
        ): selector.ObjectSelector(),
        vol.Optional(CONF_HVAC_ACTION_DP): _col_to_select(dps, is_dps=True),
        vol.Optional(
            CONF_HVAC_ACTION_SET, default=HVAC_ACTION_SETS
        ): selector.ObjectSelector(),
        vol.Optional(CONF_ECO_DP): _col_to_select(dps, is_dps=True),
        vol.Optional(CONF_ECO_VALUE): str,
        vol.Optional(CONF_PRESET_DP): _col_to_select(dps, is_dps=True),
        vol.Optional(CONF_PRESET_SET, default={}): selector.ObjectSelector(),
        vol.Optional(CONF_FAN_SPEED_DP): _col_to_select(dps, is_dps=True),
        vol.Optional(CONF_FAN_SPEED_LIST, default=FAN_SPEEDS_DEFAULT): str,
        vol.Optional(CONF_TEMPERATURE_UNIT): _col_to_select(
            [TEMPERATURE_CELSIUS, TEMPERATURE_FAHRENHEIT]
        ),
        vol.Optional(CONF_HEURISTIC_ACTION): bool,
    }


# Convertors
def f_to_c(num):
    return (num - 32) * 5 / 9


def c_to_f(num):
    return (num * 1.8) + 32


def config_unit(unit):
    if unit == TEMPERATURE_FAHRENHEIT:
        return UnitOfTemperature.FAHRENHEIT
    else:
        return UnitOfTemperature.CELSIUS


def convert_temperature(num_1, num_2) -> tuple[float, float]:
    """Take two values and compare them. If one is in Fahrenheit, Convert it to Celsius."""
    if None in (num_1, num_2):
        return num_1, num_2

    def perc_diff(value1, value2):
        """Return the percentage difference between two values"""
        max_value, min_value = max(value1, value2), min(value1, value2)
        try:
            return abs((max_value - min_value) / min_value) * 100
        except ZeroDivisionError:
            return 0

    # Check if one value is in Celsius and the other is in Fahrenheit
    if perc_diff(num_1, num_2) > 160:
        fahrenheit = max(num_1, num_2)
        to_celsius = (fahrenheit - 32) * 5 / 9
        if fahrenheit == num_1:
            num_1 = to_celsius
        elif fahrenheit == num_2:
            num_2 = to_celsius

    return num_1, num_2


class LocalTuyaClimate(LocalTuyaEntity, ClimateEntity):
    """Tuya climate device."""

    _enable_turn_on_off_backwards_compatibility = False

    def __init__(
        self,
        device,
        config_entry,
        switchid,
        **kwargs,
    ):
        """Initialize a new LocalTuyaClimate."""
        super().__init__(device, config_entry, switchid, _LOGGER, **kwargs)
        # Custom variables for Lennox
        self._device = device
        self._previous_hvac_mode = None
        self._previous_target_temp = None
        self._previous_fan_speed = None

        self._state = None
        self._target_temperature = None
        self._target_temp_forced_to_celsius = False
        self._current_temperature = None
        self._hvac_mode = None
        self._preset_mode = None
        self._hvac_action = None
        self._precision = float(self._config.get(CONF_PRECISION, DEFAULT_PRECISION))
        self._precision_target = float(
            self._config.get(CONF_TARGET_PRECISION, DEFAULT_PRECISION)
        )

        # HVAC Modes
        self._hvac_mode_dp = self._config.get(CONF_HVAC_MODE_DP)
        if modes_set := self._config.get(CONF_HVAC_MODE_SET, {}):
            # HA HVAC Modes are all lower case.
            modes_set = {k.lower(): v for k, v in modes_set.copy().items()}
        self._hvac_mode_set = modes_set

        # Presets
        self._preset_dp = self._config.get(CONF_PRESET_DP)
        self._preset_set: dict = self._config.get(CONF_PRESET_SET, {})

        # Sort Modes If the HVAC isn't supported by HA then we add it as preset.
        if self._preset_dp == self._hvac_mode_dp or not self._preset_dp:
            for k, v in self._hvac_mode_set.copy().items():
                if k not in HVACMode:
                    self._preset_dp = self._hvac_mode_dp
                    self._preset_set[k] = self._hvac_mode_set.pop(k)

        self._preset_name_to_value = {v: k for k, v in self._preset_set.items()}

        # HVAC Actions
        self._conf_hvac_action_dp = self._config.get(CONF_HVAC_ACTION_DP)
        if actions_set := self._config.get(CONF_HVAC_ACTION_SET, {}):
            actions_set = {k.lower(): v for k, v in actions_set.copy().items()}
        self._conf_hvac_action_set = actions_set

        # Fan
        self._fan_speed_dp = self._config.get(CONF_FAN_SPEED_DP)
        if fan_speeds := self._config.get(CONF_FAN_SPEED_LIST, []):
            fan_speeds = [v.lstrip() for v in fan_speeds.split(",")]
        self._fan_supported_speeds = fan_speeds
        self._has_fan_mode = self._fan_speed_dp and self._fan_supported_speeds

        # Eco!?
        self._eco_dp = self._config.get(CONF_ECO_DP)
        self._eco_value = self._config.get(CONF_ECO_VALUE, "ECO")
        self._has_presets = self._eco_dp or (self._preset_dp and self._preset_set)

        self._min_temp = self._config.get(CONF_MIN_TEMP, DEFAULT_MIN_TEMP)
        self._max_temp = self._config.get(CONF_MAX_TEMP, DEFAULT_MAX_TEMP)

        # Temperture unit
        self._temperature_unit = config_unit(self._config.get(CONF_TEMPERATURE_UNIT))

    @property
    def supported_features(self):
        """Flag supported features."""
        supported_features = ClimateEntityFeature(0)
        if self.has_config(CONF_TARGET_TEMPERATURE_DP):
            supported_features |= ClimateEntityFeature.TARGET_TEMPERATURE
        if self._has_presets:
            supported_features |= ClimateEntityFeature.PRESET_MODE
        if self._has_fan_mode:
            supported_features |= ClimateEntityFeature.FAN_MODE

        try:  # requires HA >= 2024.2.1
            supported_features |= ClimateEntityFeature.TURN_OFF
            supported_features |= ClimateEntityFeature.TURN_ON
        except AttributeError:
            ...

        return supported_features

    @property
    def precision(self):
        """Return the precision of the system."""
        return self._precision

    @property
    def temperature_unit(self):
        """Return the unit of measurement used by the platform."""
        return self._temperature_unit

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        # DEFAULT_MIN_TEMP is in C
        return self._min_temp

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        # DEFAULT_MAX_TEMP is in C
        return self._max_temp

    @property
    def hvac_mode(self):
        """Return current operation ie. heat, cool, idle."""
        if not self._state:
            return HVACMode.OFF
        if not self._hvac_mode_dp:
            return HVACMode.HEAT

        return self._hvac_mode

    @property
    def hvac_modes(self):
        """Return the list of available operation modes."""
        if not self.has_config(CONF_HVAC_MODE_DP):
            return [HVACMode.OFF]

        modes = list(self._hvac_mode_set)

        if self._config.get(CONF_HVAC_ADD_OFF, True) and HVACMode.OFF not in modes:
            modes.append(HVACMode.OFF)
        return modes

    @property
    def hvac_action(self):
        """Return the current running hvac operation if supported."""
        if not self._state:
            return HVACAction.OFF

        if not self._conf_hvac_action_dp:
            if self._hvac_mode == HVACMode.COOL:
                self._hvac_action = HVACAction.COOLING
            if self._hvac_mode == HVACMode.HEAT:
                self._hvac_action = HVACAction.HEATING
            if self._hvac_mode == HVACMode.DRY:
                self._hvac_action = HVACAction.DRYING

        # This exists from upstream, not sure the use case of this.
        if self._config.get(CONF_HEURISTIC_ACTION, False):
            if self._hvac_mode == HVACMode.HEAT:
                if self._current_temperature < (
                    self._target_temperature - self._precision
                ):
                    self._hvac_action = HVACMode.HEAT
                if self._current_temperature == (
                    self._target_temperature - self._precision
                ):
                    if self._hvac_action == HVACMode.HEAT:
                        self._hvac_action = HVACMode.HEAT
                    if self._hvac_action == HVACAction.IDLE:
                        self._hvac_action = HVACAction.IDLE
                if (
                    self._current_temperature + self._precision
                ) > self._target_temperature:
                    self._hvac_action = HVACAction.IDLE
            return self._hvac_action
        return self._hvac_action

    @property
    def preset_mode(self):
        """Return current preset."""
        mode = self.dp_value(CONF_HVAC_MODE_DP)
        if mode in list(self._hvac_mode_set.values()):
            return None

        return self._preset_mode

    @property
    def preset_modes(self):
        """Return the list of available presets modes."""
        if not self._has_presets:
            return None

        presets = list(self._preset_set.values())
        if self._eco_dp:
            presets.append(PRESET_ECO)
        return presets

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._current_temperature

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._target_temperature

    @property
    def target_temperature_step(self):
        """Return the supported step of target temperature."""
        target_step = self._config.get(CONF_TEMPERATURE_STEP, DEFAULT_TEMPERATURE_STEP)
        return float(target_step)

    @property
    def fan_mode(self):
        """Return the fan setting."""
        if not (fan_value := self.dp_value(self._fan_speed_dp)):
            return None
        return fan_value

    @property
    def fan_modes(self) -> list:
        """Return the list of available fan modes."""
        return self._fan_supported_speeds

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        if ATTR_TEMPERATURE in kwargs and self.has_config(CONF_TARGET_TEMPERATURE_DP):
            temperature = kwargs[ATTR_TEMPERATURE]

            if self._target_temp_forced_to_celsius:
                # Revert temperture to Fahrenheit it was forced to celsius
                temperature = round(c_to_f(temperature))

            temperature = round(temperature / self._precision_target)
            await self._device.set_dp(
                temperature, self._config[CONF_TARGET_TEMPERATURE_DP]
            )
            if self._state:
                await self.turn_on_led()
                await asyncio.sleep(1)
                key = self.get_key(temperature = temperature)
                _LOGGER.error("Setting key= ", key)
                data = self.get_ir_data(key)
                await self._device.set_dp("{\"head\":\"010ed80000000000040014003e00ab00ca\",\"key1\":{\"data\":\"" + data +"\",\"data_type\":0,\"key\":\"" + key + "\"},\"devid\":\"\",\"ver\":\"3\",\"delay\":300,\"control\":\"send_ir\",\"v_devid\":\"" + self._device.dev_id + "\",\"key_num\":1}\t", 201)
                await asyncio.sleep(1)
                await self.turn_off_led()

    async def async_set_fan_mode(self, fan_mode):
        """Set new target fan mode."""
        if not self._state:
            await self._device.set_dp(True, self._dp_id)

        await self._device.set_dp(fan_mode, self._fan_speed_dp)

    async def async_set_hvac_mode(self, hvac_mode: HVACMode):
        """Set new target operation mode."""
        new_states = {}
        _LOGGER.error("Requested Mode=", hvac_mode.value)
        _LOGGER.error("Current Mode=", self.hvac_mode)
        self._previous_hvac_mode = self.hvac_mode
        self._previous_target_temperature = self.target_temperature

        if not self._state and self.hvac_mode == HVACMode.OFF:
            await self._device.set_dp(True, self._dp_id)
            await asyncio.sleep(2)
        elif hvac_mode == HVACMode.OFF:
            self._previous_hvac_mode = self.hvac_mode
            self._previous_target_temperature = self.target_temperature
            await self._device.set_dp(False, self._dp_id)
            await self.async_turn_off()
            new_states[self._dp_id] = False
            return
        await self.turn_on_led()
        await asyncio.sleep(2)
        key = self.get_key(mode = hvac_mode)
        _LOGGER.error("Setting key= ", key)
        data = self.get_ir_data(key)
        await self._device.set_dp("{\"head\":\"010ed80000000000040014003e00ab00ca\",\"key1\":{\"data\":\"" + data +"\",\"data_type\":0,\"key\":\"" + key + "\"},\"devid\":\"\",\"ver\":\"3\",\"delay\":300,\"control\":\"send_ir\",\"v_devid\":\"" + self._device.dev_id + "\",\"key_num\":1}\t", 201)
        await asyncio.sleep(2)
        await self.turn_off_led()
        new_states[self._hvac_mode_dp] = self._hvac_mode_set[hvac_mode]
        await self._device.set_dps(new_states)

    async def async_turn_on(self) -> None:
        """Turn the entity on."""
        await self._device.set_dp(True, self._dp_id)
        key = self.get_key(mode = self.hvac_mode, temperature = self.target_temperature)
        data = self.get_ir_data(key)
        _LOGGER.error("Setting key= ", key)
        await self._device.set_dp("{\"head\":\"010ed80000000000040014003e00ab00ca\",\"key1\":{\"data\":\"" + data +"\",\"data_type\":0,\"key\":\"" + key + "\"},\"devid\":\"\",\"ver\":\"3\",\"delay\":300,\"control\":\"send_ir\",\"v_devid\":\"" + self._device.dev_id + "\",\"key_num\":1}\t", 201)


    async def async_turn_off(self) -> None:
        """Turn the entity off."""
        for i in range(3):
            await self._device.set_dp("{\"head\":\"010ed80000000000040014003e00ab00ca\",\"key1\":{\"data\":\"02$$0030B24D7B84E01F@%\",\"data_type\":0,\"key\":\"power_off\"},\"devid\":\"\",\"ver\":\"3\",\"delay\":300,\"control\":\"send_ir\",\"v_devid\":\"" + self._device.dev_id + "\",\"key_num\":1}", 201)
            await asyncio.sleep(1)
        await self._device.set_dp(False, self._dp_id)

    async def async_set_preset_mode(self, preset_mode):
        """Set new target preset mode."""
        if preset_mode == PRESET_ECO:
            await self._device.set_dp(self._eco_value, self._eco_dp)
            return

        preset_value = self._preset_name_to_value.get(preset_mode)
        await self._device.set_dp(preset_value, self._preset_dp)

    def status_updated(self):
        """Device status was updated."""
        self._state = self.dp_value(self._dp_id)

        # Update target temperature
        if self.has_config(CONF_TARGET_TEMPERATURE_DP):
            self._target_temperature = (
                self.dp_value(CONF_TARGET_TEMPERATURE_DP) * self._precision_target
            )

        # Update current temperature
        if self.has_config(CONF_CURRENT_TEMPERATURE_DP):
            self._current_temperature = (
                self.dp_value(CONF_CURRENT_TEMPERATURE_DP) * self._precision
            )

        # Force the Current temperature and Target temperature to matching the unit.
        target_temp, current_temperature = convert_temperature(
            self._target_temperature, self._current_temperature
        )

        # if target temperature converted to celsius, then convert all related values to set temperature.
        if target_temp != self._target_temperature:
            self._target_temperature = target_temp
            self._current_temperature = current_temperature

            if not self._target_temp_forced_to_celsius:
                self._target_temp_forced_to_celsius = True
                self._min_temp = f_to_c(self._min_temp)
                self._max_temp = f_to_c(self._max_temp)
            if self._hass.config.units == US_CUSTOMARY_SYSTEM:
                self._temperature_unit = UnitOfTemperature.CELSIUS

        # Update preset states
        if self._has_presets:
            if self.dp_value(CONF_ECO_DP) == self._eco_value:
                self._preset_mode = PRESET_ECO
            else:
                for preset_value, preset_name in self._preset_set.items():
                    if self.dp_value(CONF_PRESET_DP) == preset_value:
                        self._preset_mode = preset_name
                        break
                else:
                    self._preset_mode = PRESET_NONE

        # If device is off there is no needs to check the states.
        if not self._state:
            return

        # Update the HVAC Mode
        if self.has_config(CONF_HVAC_MODE_DP):
            for ha_hvac, tuya_value in self._hvac_mode_set.items():
                if self.dp_value(CONF_HVAC_MODE_DP) == tuya_value:
                    self._hvac_mode = ha_hvac
                    break

        # Update the current action
        if self.has_config(CONF_HVAC_ACTION_DP):
            for ha_action, tuya_value in self._conf_hvac_action_set.items():
                if self.dp_value(CONF_HVAC_ACTION_DP) == tuya_value:
                    self._hvac_action = ha_action
                    break

    def getMode(self, mode):
        match mode:
            case 'cool':
                return 0
            case 'heat':
                return 1
            case 'auto':
                return 2
            case 'fan_only':
                return 3
            case 'dry':
                return 4
            
    async def turn_on_led(self):
        _LOGGER.error("Turning on LED for %s", self._device.friendly_name)
        if self._device.friendly_name == 'Master Bedroom AC': 
            await self.toggle_helper_button('input_boolean.master_bedroom_ac_led', 'on')
        elif self._device.friendly_name == 'Bedroom 2 AC': 
            await self.toggle_helper_button('input_boolean.bedroom_2_ac_led', 'on')
        elif self._device.friendly_name == 'Bedroom 3 AC': 
            await self.toggle_helper_button('input_boolean.bedroom_3_ac_led', 'on')
        elif self._device.friendly_name == 'Living Room AC': 
            await self.toggle_helper_button('input_boolean.living_room_ac_led', 'on')

    async def turn_off_led(self):
        _LOGGER.error("Turning off LED for %s", self._device.friendly_name)
        if self._device.friendly_name == 'Master Bedroom AC': 
            await self.toggle_helper_button('input_boolean.master_bedroom_ac_led', 'off')
        elif self._device.friendly_name == 'Bedroom 2 AC': 
            await self.toggle_helper_button('input_boolean.bedroom_2_ac_led', 'off')
        elif self._device.friendly_name == 'Bedroom 3 AC': 
            await self.toggle_helper_button('input_boolean.bedroom_3_ac_led', 'off')
        elif self._device.friendly_name == 'Living Room AC': 
            await self.toggle_helper_button('input_boolean.living_room_ac_led', 'off')

    async def toggle_helper_button(self, button_name, state):
        inputStateObject = self._device._hass.states.get(button_name)
        inputState = inputStateObject.state
        inputAttributesObject = inputStateObject.attributes.copy()
        _LOGGER.error("OFF=", inputStateObject)
        if state != inputState:
            self._device._hass.states.async_set(button_name, state, inputAttributesObject)

    def get_key(self, **kwargs):
        mode = kwargs.get('mode', self.hvac_mode)
        _LOGGER.error("get_key", mode)
        temperature = kwargs.get('temperature', self._target_temperature)
        key = "M" + str(self.getMode(mode))
        if self.hvac_mode is not 'fan_only':
            key = key + "_" + "T" + str(round(temperature))
        if self.hvac_mode != 'auto' and self.hvac_mode != 'dry':
            key = key + "_" + "S" + str(0)
        _LOGGER.error("on=",key)
        return key
    
    def get_ir_data(self, key):
        data = '02$$0030B24DBF407C83@%'
        match key:
            case 'M4_T17':
                data = '02$$0030B24D1FE004FB@%'
            case 'M4_T18':
                data = '02$$0030B24D1FE014EB@%'
            case 'M4_T19':
                data = '02$$0030B24D1FE034CB@%'
            case 'M4_T20':
                data = '02$$0030B24D1FE024DB@%'
            case 'M4_T21':
                data = '02$$0030B24D1FE0649B@%'
            case 'M4_T22':
                data = '02$$0030B24D1FE0748B@%'
            case 'M4_T23':
                data = '02$$0030B24D1FE054AB@%'
            case 'M4_T24':
                data = '02$$0030B24D1FE044BB@%'
            case 'M4_T25':
                data = '02$$0030B24D1FE0C43B@%'
            case 'M4_T26':
                data = '02$$0030B24D1FE0D42B@%'
            case 'M4_T27':
                data = '02$$0030B24D1FE0946B@%'
            case 'M4_T28':
                data = '02$$0030B24D1FE0847B@%'
            case 'M4_T29':
                data = '02$$0030B24D1FE0A45B@%'
            case 'M4_T30':
                data = '02$$0030B24D1FE0B44B@%'
            case 'M0_T17_S0':
                data = '02$$0030B24DBF4000FF@%'
            case 'M0_T18_S0':
                data = '02$$0030B24DBF4010EF@%'
            case 'M0_T19_S0':
                data = '02$$0030B24DBF4030CF@%'
            case 'M0_T20_S0':
                data = '02$$0030B24DBF4020DF@%'
            case 'M0_T21_S0':
                data = '02$$0030B24DBF40609F@%'
            case 'M0_T22_S0':
                data = '02$$0030B24DBF40708F@%'
            case 'M0_T23_S0':
                data = '02$$0030B24DBF4050AF@%'
            case 'M0_T24_S0':
                data = '02$$0030B24DBF4040BF@%'
            case 'M0_T25_S0':
                data = '02$$0030B24DBF40C03F@%'
            case 'M0_T26_S0':
                data = '02$$0030B24DBF40D02F@%'
            case 'M0_T27_S0':
                data = '02$$0030B24DBF40906F@%'
            case 'M0_T28_S0':
                data = '02$$0030B24DBF40807F@%'
            case 'M0_T29_S0':
                data = '02$$0030B24DBF40A05F@%'
            case 'M0_T30_S0':
                data = '02$$0030B24DBF40B04F@%'
            case 'M2_T17':
                data = '02$$0030B24D1FE008F7@%'
            case 'M2_T18':
                data = '02$$0030B24D1FE018E7@%'
            case 'M2_T19':
                data = '02$$0030B24D1FE038C7@%'
            case 'M2_T20':
                data = '02$$0030B24D1FE028D7@%'
            case 'M2_T21':
                data = '02$$0030B24D1FE06897@%'
            case 'M2_T22':
                data = '02$$0030B24D1FE07887@%'
            case 'M2_T23':
                data = '02$$0030B24D1FE058A7@%'
            case 'M2_T24':
                data = '02$$0030B24D1FE048B7@%'
            case 'M2_T25':
                data = '02$$0030B24D1FE0C837@%'
            case 'M2_T26':
                data = '02$$0030B24D1FE0D827@%'
            case 'M2_T27':
                data = '02$$0030B24D1FE09867@%'
            case 'M2_T28':
                data = '02$$0030B24D1FE08877@%'
            case 'M2_T29':
                data = '02$$0030B24D1FE0A857@%'
            case 'M2_T30':
                data = '02$$0030B24D1FE0B847@%'
            case 'M1_T17_S0':
                data = '02$$0030B24DBF400CF3@%'
            case 'M1_T18_S0':
                data = '02$$0030B24DBF401CE3@%'
            case 'M1_T19_S0':
                data = '02$$0030B24DBF403CC3@%'
            case 'M1_T20_S0':
                data = '02$$0030B24DBF402CD3@%'
            case 'M1_T21_S0':
                data = '02$$0030B24DBF406C93@%'
            case 'M1_T22_S0':
                data = '02$$0030B24DBF407C83@%'
            case 'M1_T23_S0':
                data = '02$$0030B24DBF405CA3@%'
            case 'M1_T24_S0':
                data = '02$$0030B24DBF404CB3@%'
            case 'M1_T25_S0':
                data = '02$$0030B24DBF40CC33@%'
            case 'M1_T26_S0':
                data = '02$$0030B24DBF40DC23@%'
            case 'M1_T27_S0':
                data = '02$$0030B24DBF409C63@%'
            case 'M1_T28_S0':
                data = '02$$0030B24DBF408C73@%'
            case 'M1_T29_S0':
                data = '02$$0030B24DBF40AC53@%'
            case 'M1_T30_S0':
                data = '02$$0030B24DBF40BC43@%'
            case 'M3_S0':
                data = '02$$0030B24DBF40E41B@%'
        return data


async_setup_entry = partial(async_setup_entry, DOMAIN, LocalTuyaClimate, flow_schema)
