"""Platform to locally control Tuya-based button devices."""

import logging
from functools import partial

import voluptuous as vol
from homeassistant.components.button import DOMAIN, ButtonEntity
from homeassistant.util import dt as dt_util

from .entity import LocalTuyaEntity, async_setup_entry
from .const import CONF_PASSIVE_ENTITY

_LOGGER = logging.getLogger(__name__)


def flow_schema(dps):
    """Return schema used in config flow."""
    return {
        # vol.Required(CONF_PASSIVE_ENTITY): bool,
    }


class LocalTuyaButton(LocalTuyaEntity, ButtonEntity):
    """Representation of a Tuya button."""

    def __init__(
        self,
        device,
        config_entry,
        buttonid,
        **kwargs,
    ):
        """Initialize the Tuya button."""
        super().__init__(device, config_entry, buttonid, _LOGGER, **kwargs)
        self._state = None

    async def async_press(self):
        """Press the button."""
        await self._device.set_dp(True, self._dp_id)

    def status_updated(self):
        """Device status was updated."""
        super().status_updated()
        state = str(self.dp_value(self._dp_id)).lower()
        self._ButtonEntity__set_state(f"{state}_{dt_util.utcnow().isoformat()}")
        self._status.pop(self._dp_id, None)

async_setup_entry = partial(async_setup_entry, DOMAIN, LocalTuyaButton, flow_schema)
