from __future__ import annotations
from datetime import timedelta

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, LOGGER
from .ekenergo import Ekenergo


PLATFORMS: list[str] = [Platform.SENSOR, Platform.BUTTON, Platform.NUMBER]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    ee = Ekenergo(entry.data.get("account"), entry.data.get("phone"))
    coordinator = Coordinator(hass, LOGGER, name=ee.get("account"), update_method=ee.pull, update_interval=timedelta(days=7))

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "ee": ee,
        "coordinator": coordinator,
    }

    try:
        await coordinator.async_config_entry_first_refresh()

    except Exception:
        return False

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

class Coordinator(DataUpdateCoordinator):
    def __init__(self, hass, logger, name, update_interval, update_method):
        super().__init__(hass=hass, logger=logger, name=name, update_interval=update_interval, update_method=update_method)
        self._entity_callback = {}

    def entity_callback_register(self, name, callback):
        self._entity_callback[name] = callback

    def entity_callback_call(self, name):
        self._entity_callback[name]()
