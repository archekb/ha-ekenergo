from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, LOGGER


# async def async_setup_platform(hass: HomeAssistant, config, async_add_entities, discovery_info=None):
#     LOGGER.critical("Sensors configuration via configuration.yaml are not supported!")
#     return False

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    ee = hass.data[DOMAIN].get(entry.entry_id).get("ee")
    coordinator = hass.data[DOMAIN].get(entry.entry_id).get("coordinator")

    new_sensors = [
        LastUpdate(coordinator, ee),
        LastSended(coordinator, ee),
        Address(coordinator, ee),
        District(coordinator, ee),
        Debt(coordinator, ee),
        Manager(coordinator, ee),
        ManagerPhone(coordinator, ee),
        Account(coordinator, ee)
    ]

    for iname in ee.get("indicator_data").keys():
        new_sensors.append(Indicator(coordinator, ee, iname))

    async_add_entities(new_sensors)
    return True

class Default(SensorEntity, CoordinatorEntity):
    @property
    def device_info(self):
        return self._ee.deviceInfo()

    def _handle_coordinator_update(self) -> None:
        self._attr_assumed_state = False if self.coordinator.last_update_success else True
        self.async_write_ha_state()

class LastUpdate(Default):
    _attr_icon = "mdi:calendar-clock"

    def __init__(self, coordinator, ee):
        CoordinatorEntity.__init__(self=self, coordinator=coordinator)
        self._ee = ee
        self._attr_unique_id = f"{DOMAIN}_{self._ee.get('account')}_last_update"
        self._attr_name = f"{DOMAIN}_{self._ee.get('account')} Дата обновления"

    @property
    def state(self):
        last_update = self._ee.get("last_update")
        return  last_update if last_update is None else last_update.strftime("%y.%m.%d %H:%M:%S")

class LastSended(Default):
    _attr_icon = "mdi:calendar-clock"

    def __init__(self, coordinator, ee):
        CoordinatorEntity.__init__(self=self, coordinator=coordinator)
        coordinator.entity_callback_register(f"{DOMAIN}_{ee.get('account')}_last_send", self.async_write_ha_state)
        self._ee = ee
        self._attr_unique_id = f"{DOMAIN}_{self._ee.get('account')}_last_send"
        self._attr_name = f"{DOMAIN}_{self._ee.get('account')} Дата отправки"

    @property
    def state(self):
        last_send = self._ee.get("last_send")
        return  last_send if last_send is None else last_send.strftime("%y.%m.%d %H:%M:%S")
  

class Address(Default):
    _attr_icon = "mdi:map-marker"

    def __init__(self, coordinator, ee):
        CoordinatorEntity.__init__(self=self, coordinator=coordinator)
        self._ee = ee
        self._attr_unique_id = f"{DOMAIN}_{self._ee.get('account')}_address"
        self._attr_name = f"{DOMAIN}_{self._ee.get('account')} Адрес"

    @property
    def state(self):
        return self._ee.get("address")

class District(Default):
    _attr_icon = "mdi:map-marker"

    def __init__(self, coordinator, ee):
        CoordinatorEntity.__init__(self=self, coordinator=coordinator)
        self._ee = ee
        self._attr_unique_id = f"{DOMAIN}_{self._ee.get('account')}_district"
        self._attr_name = f"{DOMAIN}_{self._ee.get('account')} Район"

    @property
    def state(self):
        return self._ee.get("district")

class Debt(Default):
    _attr_icon = "mdi:cash-multiple"
    _attr_native_unit_of_measurement = 'руб.'

    def __init__(self, coordinator, ee):
        CoordinatorEntity.__init__(self=self, coordinator=coordinator)
        self._ee = ee
        self._attr_unique_id = f"{DOMAIN}_{self._ee.get('account')}_debt"
        self._attr_name = f"{DOMAIN}_{self._ee.get('account')} Задолженость"

    @property
    def state(self):
        return self._ee.get("debt")

class Manager(Default):
    _attr_icon = "mdi:account"

    def __init__(self, coordinator, ee):
        CoordinatorEntity.__init__(self=self, coordinator=coordinator)
        self._ee = ee
        self._attr_unique_id = f"{DOMAIN}_{self._ee.get('account')}_manager"
        self._attr_name = f"{DOMAIN}_{self._ee.get('account')} Представитель"

    @property
    def state(self):
        return self._ee.get("manager")

class ManagerPhone(Default):
    _attr_icon = "mdi:phone"

    def __init__(self, coordinator, ee):
        CoordinatorEntity.__init__(self=self, coordinator=coordinator)
        self._ee = ee
        self._attr_unique_id = f"{DOMAIN}_{self._ee.get('account')}_manager_phone"
        self._attr_name = f"{DOMAIN}_{self._ee.get('account')} Телефон"

    @property
    def state(self):
        return self._ee.get("phone")

class Account(Default):
    _attr_icon = "mdi:account"

    def __init__(self, coordinator, ee):
        CoordinatorEntity.__init__(self=self, coordinator=coordinator)
        self._ee = ee
        self._attr_unique_id = f"{DOMAIN}_{self._ee.get('account')}_account"
        self._attr_name = f"{DOMAIN}_{self._ee.get('account')} Номер счета"

    @property
    def state(self):
        return self._ee.get("account")

class Indicator(Default):
    _attr_icon = "mdi:counter"
    _attr_native_unit_of_measurement = 'кВт/ч'

    def __init__(self, coordinator, ee, iname: str):
        CoordinatorEntity.__init__(self=self, coordinator=coordinator)
        self._ee = ee
        self._iname = iname
        self._attr_unique_id = f"{DOMAIN}_{self._ee.get('account')}_indicator_{self._iname}"
        self._attr_name = f"{DOMAIN}_{self._ee.get('account')} {self._ee.get(f'indicator_data.{self._iname}.name')}"

    @property
    def state(self):
        return self._ee.get(f'indicator_data.{self._iname}.value')

    @property
    def extra_state_attributes(self):
        return self._ee.get(f'indicator_data.{self._iname}.attrs')

