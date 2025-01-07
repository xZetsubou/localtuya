"""Platform to present any Tuya DP as a binary sensor."""

import logging
from functools import partial

import voluptuous as vol
from homeassistant.components.binary_sensor import (
    DEVICE_CLASSES_SCHEMA,
    DOMAIN,
    BinarySensorEntity,
)
from homeassistant.const import CONF_DEVICE_CLASS

from .entity import LocalTuyaEntity, async_setup_entry
from .const import CONF_STATE_ON

_LOGGER = logging.getLogger(__name__)

CONF_STATE_OFF = "state_off"


def flow_schema(dps):
    """Return schema used in config flow."""
    return {
        vol.Required(CONF_STATE_ON, default="True"): str,
        # vol.Required(CONF_STATE_OFF, default="False"): str,
        vol.Optional(CONF_DEVICE_CLASS): DEVICE_CLASSES_SCHEMA,
    }


class LocalTuyaBinarySensor(LocalTuyaEntity, BinarySensorEntity):
    """Representation of a Tuya binary sensor."""

    def __init__(
        self,
        device,
        config_entry,
        sensorid,
        **kwargs,
    ):
        """Initialize the Tuya binary sensor."""
        super().__init__(device, config_entry, sensorid, _LOGGER, **kwargs)
        self._is_on = False

    @property
    def is_on(self):
        """Return sensor state."""
        return self._is_on

    def status_updated(self):
        """Update device status and determine if sensor is on."""
        super().status_updated()

        state = str(self.dp_value(self._dp_id)).lower()
        configured_on_state = self._config[CONF_STATE_ON].lower()
        self._is_on = state == configured_on_state or state in {
            "true",
            "1",
            "pir",
            "on",
        }


async_setup_entry = partial(
    async_setup_entry, DOMAIN, LocalTuyaBinarySensor, flow_schema
)
