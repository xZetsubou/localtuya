"""Platform to present any Tuya DP as a remote."""

import asyncio
import json
import base64
import logging
from functools import partial
import struct
from enum import StrEnum
from typing import Any, Iterable
from .config_flow import _col_to_select

import voluptuous as vol
from homeassistant.components.remote import (
    ATTR_ACTIVITY,
    ATTR_COMMAND,
    ATTR_COMMAND_TYPE,
    ATTR_NUM_REPEATS,
    ATTR_DELAY_SECS,
    ATTR_DEVICE,
    ATTR_TIMEOUT,
    DOMAIN,
    RemoteEntity,
    RemoteEntityFeature,
)
from homeassistant.components import persistent_notification
from homeassistant.const import CONF_DEVICE_ID, STATE_OFF
from homeassistant.core import HomeAssistant, State
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers.storage import Store

from .entity import LocalTuyaEntity, async_setup_entry
from .const import CONF_RECEIVE_DP, CONF_KEY_STUDY_DP

NSDP_CONTROL = "control"  # The control commands
NSDP_TYPE = "type"  # The identifier of an IR library
NSDP_HEAD = "head"  # Actually used but not documented
NSDP_KEY1 = "key1"  # Actually used but not documented

_LOGGER = logging.getLogger(__name__)


class ControlType(StrEnum):
    ENUM = "Enum"
    JSON = "Json"


class ControlMode(StrEnum):
    SEND_IR = "send_ir"
    STUDY = "study"
    STUDY_EXIT = "study_exit"
    STUDY_KEY = "study_key"


class RemoteDP(StrEnum):
    DP_SEND = "201"
    DP_RECIEVE = "202"


MODE_IR_TO_RF = {
    ControlMode.SEND_IR: "rfstudy_send",
    ControlMode.STUDY: "rf_study",
    ControlMode.STUDY_EXIT: "rfstudy_exit",
    ControlMode.STUDY_KEY: "rf_study",
}

MODE_RF_TO_SHORT = {
    MODE_IR_TO_RF[ControlMode.STUDY]: "rf_shortstudy",
    MODE_IR_TO_RF[ControlMode.STUDY_EXIT]: "rfstudy_exit",
}
ATTR_FREQ = "freq"
ATTR_VER = "ver"
ATTR_RF_TYPE = "rf_type"

CODE_STORAGE_VERSION = 1
SOTRAGE_KEY = "localtuya_remotes_codes"


def flow_schema(dps):
    """Return schema used in config flow."""
    return {
        vol.Optional(
            CONF_RECEIVE_DP, default=RemoteDP.DP_RECIEVE.value
        ): _col_to_select(dps, is_dps=True),
        vol.Optional(CONF_KEY_STUDY_DP): _col_to_select(dps, is_dps=True),
    }


class LocalTuyaRemote(LocalTuyaEntity, RemoteEntity):
    """Representation of a Tuya remote."""

    def __init__(
        self,
        device,
        config_entry,
        remoteid,
        **kwargs,
    ):
        """Initialize the Tuya remote."""
        super().__init__(device, config_entry, remoteid, _LOGGER, **kwargs)

        self._dp_send = str(self._config.get(self._dp_id, RemoteDP.DP_SEND))
        self._dp_recieve = str(self._config.get(CONF_RECEIVE_DP, RemoteDP.DP_RECIEVE))
        self._dp_key_study = self._config.get(CONF_KEY_STUDY_DP)

        self._device_id = self._device_config.id

        # self._attr_activity_list: list = []
        # self._attr_current_activity: str | None = None

        self._last_code = None

        self._codes = {}  # Contains only device commands.
        self._global_codes = {}  # contains all devices commands.

        self._codes_storage = Store(self._hass, CODE_STORAGE_VERSION, SOTRAGE_KEY)

        self._storage_loaded = False

        self._attr_supported_features = (
            RemoteEntityFeature.LEARN_COMMAND | RemoteEntityFeature.DELETE_COMMAND
        )

    @property
    def _ir_control_type(self):
        if self.has_config(CONF_KEY_STUDY_DP):
            return ControlType.ENUM
        else:
            return ControlType.JSON

    @staticmethod
    def rf_decode_button(base64_code):
        try:
            jstr = base64.b64decode
            jdata = json.loads(jstr)
            return jdata
        except:
            return None

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the remote."""
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the remote."""
        self._attr_is_on = False
        self.async_write_ha_state()

    async def async_send_command(self, command: Iterable[str], **kwargs: Any) -> None:
        """Send commands to a device."""
        if not self._attr_is_on:
            raise ServiceValidationError(f"Remote {self.entity_id} is turned off")

        commands = command
        device = kwargs.get(ATTR_DEVICE)

        repeats: int = kwargs.get(ATTR_NUM_REPEATS)
        repeats_delay: float = kwargs.get(ATTR_DELAY_SECS)

        for req in [device, commands]:
            if not req:
                raise ServiceValidationError("Missing required fields")

        if not self._storage_loaded:
            await self._async_load_storage()

        # base64_code = ""
        # if base64_code is None:
        #     option_value = ""
        #     _LOGGER.debug("Sending Option: -> " + option_value)

        #     pulses = self.pronto_to_pulses(option_value)
        #     base64_code = "1" + self.pulses_to_base64(pulses)
        for command in commands:
            code, is_rf = self._get_code(device, command)

            base64_code = "1" + code
            if repeats:
                current_repeat = 0
                while current_repeat < repeats:
                    await self.send_signal(ControlMode.SEND_IR, base64_code, rf=is_rf)
                    if repeats_delay:
                        await asyncio.sleep(repeats_delay)
                    current_repeat += 1
                continue

            await self.send_signal(ControlMode.SEND_IR, base64_code)

    async def async_learn_command(self, **kwargs: Any) -> None:
        """Learn a command from a device."""
        if not self._attr_is_on:
            raise ServiceValidationError(f"Remote {self.entity_id} is turned off")

        now, timeout = 0, kwargs.get(ATTR_TIMEOUT, 30)
        sucess = False

        device = kwargs.get(ATTR_DEVICE)
        commands = kwargs.get(ATTR_COMMAND)

        is_rf = kwargs.get(ATTR_COMMAND_TYPE) == "rf"
        _LOGGER.debug(f"IS RF??? : {is_rf}")
        # command_type = kwargs.get(ATTR_COMMAND_TYPE)
        for req in [device, commands]:
            if not req:
                raise ServiceValidationError("Missing required fields")

        if not self._storage_loaded:
            await self._async_load_storage()

        for command in commands:
            last_code = self._last_code
            await self.send_signal(ControlMode.STUDY, rf=is_rf)
            persistent_notification.async_create(
                self.hass,
                f"Press the '{command}' button.",
                title="Learn command",
                notification_id="learn_command",
            )

            try:
                self.debug(f"Waiting for code from DP: {self._dp_recieve}")
                while now < timeout:
                    if last_code != (dp_code := self.dp_value(self._dp_recieve)):
                        self._last_code = dp_code
                        sucess = True
                        await self.send_signal(ControlMode.STUDY_EXIT, rf=is_rf)
                        break

                    now += 1
                    await asyncio.sleep(1)

                if not sucess:
                    raise ServiceValidationError(f"Failed to learn: {command}")

            finally:
                await self.send_signal(ControlMode.STUDY_EXIT, rf=is_rf)
                persistent_notification.async_dismiss(
                    self.hass, notification_id="learn_command"
                )

            # code retrive sucess and it's sotred in self._last_code
            # we will store the codes.
            await self._save_new_command(device, command, self._last_code)

            if command != commands[-1]:
                await asyncio.sleep(1)

    async def async_delete_command(self, **kwargs: Any) -> None:
        """Delete commands from the database."""
        device = kwargs.get(ATTR_DEVICE)
        commands = kwargs.get(ATTR_COMMAND)

        for req in [device, commands]:
            if not req:
                raise ServiceValidationError("Missing required fields")

        if not self._storage_loaded:
            await self._async_load_storage()

        for command in commands:
            await self._delete_command(device, command)

    async def send_signal(self, control, base64_code=None, rf=False):
        if self._ir_control_type == ControlType.ENUM:
            command = {self._dp_id: control}
            if control == ControlMode.SEND_IR:
                command[self._dp_id] = ControlMode.STUDY_KEY.value
                command[self._dp_key_study] = base64_code
        else:
            command = {NSDP_CONTROL: control if not rf else MODE_IR_TO_RF.get(control)}
            if control == ControlMode.SEND_IR:
                # command[NSDP_TYPE] = 0
                # command[NSDP_HEAD] = ""  # also known as ir_code
                command[NSDP_KEY1] = base64_code  # also code: key_code
            if rf:
                command[ATTR_FREQ] = "0"
                if ATTR_RF_TYPE not in command or not command[ATTR_RF_TYPE]:
                    command[ATTR_RF_TYPE] = "sub_2g"
                if ATTR_FREQ not in command or not command[ATTR_FREQ]:
                    command[ATTR_FREQ] = "0"
                if ATTR_VER not in command or not command[ATTR_VER]:
                    command[ATTR_VER] = "2"
            command = {self._dp_id: json.dumps(command)}

        self.debug(f"Sending Command: {command}")
        if rf and base64_code:
            decoded_code = self.rf_decode_button(base64_code)
            self.debug(f"Decoded RF Button: {decoded_code}")

        await self._device.set_dps(command)

    async def _delete_command(self, device, command) -> None:
        """Store new code into stoarge."""
        codes_data = self._codes
        ir_controller = self._device_id
        devices_data = self._global_codes

        if ir_controller in codes_data:
            devices_data = codes_data[ir_controller]

        if device not in devices_data:
            raise ServiceValidationError(
                f"Couldn't find the device: {device} available devices is on this IR Remote is: {list(devices_data)}."
            )

        commands = devices_data[device]
        if command not in commands:
            commands.pop("rf", False)
            raise ServiceValidationError(
                f"Couldn't find the command {command} for in {device} device. the available commands for this device is: {list(commands)}"
            )

        # For now this only works if the command is in the list of commands of this device.
        devices_data[device].pop(command)
        if device in self._global_codes:
            self._global_codes.pop(device)
        await self._codes_storage.async_save(codes_data)

    async def _save_new_command(self, device, command, code) -> None:
        """Store new code into stoarge."""
        device_unqiue_id = self._device_id
        codes = self._codes

        if device_unqiue_id not in codes:
            codes[device_unqiue_id] = {}

        # device_data = {command: {ATTR_COMMAND: code, ATTR_COMMAND_TYPE: command_type}}
        device_data = {command: code}

        if device in codes[device_unqiue_id]:
            codes[device_unqiue_id][device].update(device_data)
        else:
            codes[device_unqiue_id][device] = device_data

        self._global_codes[device] = device_data
        await self._codes_storage.async_save(codes)

    async def _async_load_storage(self):
        """Load code and flag storage from disk."""
        # Exception is intentionally not trapped to
        # provide feedback if something fails.
        # await self._codes_storage._async_migrate_func(1, 1, self._codes)
        self._codes.update(await self._codes_storage.async_load() or {})

        if self._codes:
            for dev in self._codes.keys():
                self._global_codes.update(self._codes[dev])

        self._storage_loaded = True

    # No need to restore state for a remote
    async def restore_state_when_connected(self):
        """Do nothing for a remote."""
        return

    def _get_code(self, device, command):
        """Get the code of command from database."""
        codes_data = self._codes
        ir_controller = self._device_id
        devices_data = self._global_codes

        if ir_controller in codes_data:
            devices_data = codes_data[ir_controller]

        if device not in devices_data:
            raise ServiceValidationError(
                f"Couldn't find the device: {device} available devices is on this IR Remote is: {list(devices_data)}."
            )

        commands = devices_data[device]
        if command not in commands:
            commands.pop("rf", False)
            raise ServiceValidationError(
                f"Couldn't find the command {command} for in {device} device. the available commands for this device is: {list(commands)}"
            )

        command = devices_data[device][command]
        is_rf = devices_data[device].get("rf")

        return command, is_rf

    async def _async_migrate_func(self, old_major_version, old_minor_version, old_data):
        """Migrate to the new version."""
        raise NotImplementedError

    def status_updated(self):
        """Device status was updated."""
        state = self.dp_value(self._dp_id)

    def status_restored(self, stored_state: State) -> None:
        """Device status was restored.."""
        state = stored_state
        self._attr_is_on = state is None or state.state != STATE_OFF


async_setup_entry = partial(async_setup_entry, DOMAIN, LocalTuyaRemote, flow_schema)
