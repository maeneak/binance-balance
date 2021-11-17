"""Sensor platform for Binance Balance."""
from .const import DEFAULT_NAME
from .const import DOMAIN
from .const import NAME
from .const import ICON
from .const import SENSOR
from .entity import BinanceBalanceEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([BinanceBalanceSensor(coordinator, entry)])


class BinanceBalanceSensor(BinanceBalanceEntity):
    """binance_balance Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DOMAIN}_spot"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON

    @property
    def unit_of_measurement(self):
        """Return the icon of the sensor."""
        return "BTC"

    @property
    def device_class(self):
        """Return de device class of the sensor."""
        return "binance_balance__custom_device_class"
