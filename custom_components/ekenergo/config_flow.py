from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant

from .const import DOMAIN, LOGGER
from .ekenergo import Ekenergo


DATA_SCHEMA = vol.Schema({
    vol.Required("account"): str,
    vol.Optional("phone", description="(optional) Phone number which will send to provider"): str,
})


async def validate_input(data: dict) -> dict[str, Any]:
    if data.get("account", "").isdigit() != True:
        raise ErrorInvalidAccount

    ee = Ekenergo(data.get("account"), data.get("phone"))
    if not await ee.isExist():
        raise ErrorAccountNotFound

    return {"account": data.get("account"), "phone": data.get("phone")}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                cnf = await validate_input(user_input)
                for entry in self._async_current_entries():
                    if entry.data.get("account") == cnf.get("account"):
                        raise ErrorAlreadyAdded

                await self.async_set_unique_id(cnf.get("account"))
                return self.async_create_entry(title=cnf.get("account"), data=cnf)

            except ErrorAccountNotFound:
                errors["account"] = "account_not_found"

            except ErrorInvalidAccount:
                errors["account"] = "account_invalid"

            except ErrorAlreadyAdded:
                errors["account"] = "already_added"

            except Exception:
                LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form( step_id="user", data_schema=DATA_SCHEMA, errors=errors )

class ErrorInvalidAccount(exceptions.HomeAssistantError):
    """Error invalid Ekenergo Account."""

class ErrorAccountNotFound(exceptions.HomeAssistantError):
    """Error Ekenergo Account not found."""

class ErrorAlreadyAdded(exceptions.HomeAssistantError):
    """Error Ekenergo Account already found."""
