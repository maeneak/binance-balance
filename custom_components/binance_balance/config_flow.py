"""Adds config flow for Binance Balance."""
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from .api import BinanceBalanceApiClient
from .const import CONF_API_SECRET
from .const import CONF_API_KEY
from .const import CONF_EXHANGE
from .const import DOMAIN
from .const import DOMAIN_NAME
from .const import NAME
from .const import PLATFORMS


class BinanceBalanceFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for binance_balance."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        # if self._async_current_entries():
        #     return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            valid = await self._test_credentials(
                user_input[CONF_API_KEY], user_input[CONF_API_SECRET]
            )
            if valid:
                return self.async_create_entry(title=DOMAIN_NAME, data=user_input)
            else:
                self._errors["base"] = "auth"

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return BinanceBalanceOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        exchanges = ["com", "eu", "us", "jp"]
        default_exchange = "com"

        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                    vol.Required(CONF_API_SECRET): str,
                    vol.Required(CONF_EXHANGE, default=default_exchange): vol.In(
                        exchanges
                    ),
                }
            ),
            errors=self._errors,
        )

    async def _test_credentials(self, key, secret):
        """Return true if credentials is valid."""
        try:
            # session = async_create_clientsession(self.hass)
            # client = BinanceBalanceApiClient(username, password, session)
            # await client.async_get_data()
            return True
        except Exception:  # pylint: disable=broad-except
            pass
        return False


class BinanceBalanceOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for binance_balance."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(x, default=self.options.get(x, True)): bool
                    for x in sorted(PLATFORMS)
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(DOMAIN_NAME), data=self.options
        )
