
from homeassistant.components.number import NumberEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    ee = hass.data[DOMAIN].get(entry.entry_id).get("ee")

    new_inputs = []
    for iname in ee.get("indicator_data").keys():
        new_inputs.append(IndicatorInput(ee, iname))

    async_add_entities(new_inputs)
    return True
    
class IndicatorInput(NumberEntity):
    _attr_icon = "mdi:counter"
    _attr_native_unit_of_measurement = 'кВт/ч'

    def __init__(self, ee, iname):
        self._ee = ee
        self._iname = iname
        self._attr_unique_id = f"{DOMAIN}_{self._ee.get('account')}_indicator_{self._iname}_input"
        self._attr_name = f"{DOMAIN}_{self._ee.get('account')}  {self._ee.get(f'indicator_data.{self._iname}.name')}"
        self._attr_native_min_value = 0
        self._attr_native_max_value = 99999999
        self._attr_native_step = 1
        self._attr_mode = "box"

    @property
    def device_info(self):
        return self._ee.deviceInfo()

    @property
    def native_value(self):
        return self._ee.get(f'indicator_data.{self._iname}.new_value')

    async def async_set_native_value(self, value: float) -> None:
        self._ee.setIndicator(self._iname, int(value))
        self.async_write_ha_state()
