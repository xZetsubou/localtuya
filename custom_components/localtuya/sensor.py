"""Platform to present any Tuya DP as a sensor."""

import logging
from functools import partial
from .config_flow import col_to_select

import voluptuous as vol
from homeassistant.components.sensor import (
    DEVICE_CLASSES_SCHEMA,
    DOMAIN,
    STATE_CLASSES_SCHEMA,
    SensorStateClass,
    SensorEntity,
)
from homeassistant.const import (
    CONF_DEVICE_CLASS,
    CONF_UNIT_OF_MEASUREMENT,
    STATE_UNKNOWN,
)

from .entity import LocalTuyaEntity, async_setup_entry
from .const import CONF_SCALING, CONF_STATE_CLASS

_LOGGER = logging.getLogger(__name__)

DEFAULT_PRECISION = 2


def flow_schema(dps):
    """Return schema used in config flow."""
    return {
        vol.Optional(CONF_UNIT_OF_MEASUREMENT): str,
        vol.Optional(CONF_DEVICE_CLASS): DEVICE_CLASSES_SCHEMA,
        vol.Optional(CONF_STATE_CLASS): col_to_select(
            [sc.value for sc in SensorStateClass]
        ),
        vol.Optional(CONF_SCALING, default=1.0): vol.All(
            vol.Coerce(float), vol.Range(min=-1000000.0, max=1000000.0)
        ),
    }


class LocalTuyaSensor(LocalTuyaEntity, SensorEntity):
    """Representation of a Tuya sensor."""

    def __init__(
        self,
        device,
        config_entry,
        sensorid,
        **kwargs,
    ):
        """Initialize the Tuya sensor."""
        super().__init__(device, config_entry, sensorid, _LOGGER, **kwargs)
        self._state = None

    @property
    def native_value(self):
        """Return sensor state."""
        return self._state

    @property
    def device_class(self):
        """Return the class of this device."""
        return self._config.get(CONF_DEVICE_CLASS)

    @property
    def state_class(self) -> str | None:
        """Return state class."""
        return self._config.get(CONF_STATE_CLASS)

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._config.get(CONF_UNIT_OF_MEASUREMENT)

    def status_updated(self):
        """Update sensor state with scaled value."""
        raw_state = self.dp_value(self._dp_id)
        self._state = self._scale_value(raw_state)

    def _scale_value(self, value):
        """Scale the raw value using configured scaling."""
        scaling_factor = self._config.get(CONF_SCALING, 1.0)
        try:
            return round(value * scaling_factor, DEFAULT_PRECISION)
        except (TypeError, ValueError) as e:
            _LOGGER.warning("Failed to scale value %s: %s", value, e)
            return STATE_UNKNOWN


async_setup_entry = partial(async_setup_entry, DOMAIN, LocalTuyaSensor, flow_schema)
