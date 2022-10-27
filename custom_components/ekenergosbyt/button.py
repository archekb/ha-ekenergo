from homeassistant.components.button import  ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, LOGGER


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    ee = hass.data[DOMAIN].get(entry.entry_id).get("ee")
    coordinator = hass.data[DOMAIN].get(entry.entry_id).get("coordinator")

    new_buttons = [
        PullButton(coordinator, ee),
        PushButton(coordinator, ee)
    ]
    async_add_entities(new_buttons)

    return True

class PullButton(ButtonEntity):
    def __init__(self, coordinator, ee):
        self._ee = ee
        self._coordinator = coordinator
        self._attr_unique_id = f"{DOMAIN}_{self._ee.get('account')}_pull_button"
        self._attr_name = f"{DOMAIN}_{self._ee.get('account')} Обновить данные"

    @property
    def device_info(self):
        return self._ee.deviceInfo()

    async def async_press(self) -> None:
        await self._coordinator.async_refresh()

class PushButton(ButtonEntity):
    def __init__(self, coordinator, ee):
        self._ee = ee
        self._coordinator = coordinator
        self._attr_unique_id = f"{DOMAIN}_{self._ee.get('account')}_push_button"
        self._attr_name = f"{DOMAIN}_{self._ee.get('account')} Отправить показания"

    @property
    def device_info(self):
        return self._ee.deviceInfo()

    async def async_press(self) -> None:
        await self._ee.push()
        self._coordinator.entity_callback_call(f"{DOMAIN}_{self._ee.get('account')}_last_send")

