"""Constants for Binance Balance."""
# Base component constants
NAME = "Binance Balance"
DOMAIN_NAME = "Binance"
DOMAIN = "binance_balance"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"

ATTRIBUTION = "Data provided by http://binance.com/"
ISSUE_URL = "https://github.com/maeneak/binance-balance/issues"

# Icons
ICON = "mdi:currency-btc"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
SWITCH = "switch"
PLATFORMS = [SENSOR]


# Configuration and options
CONF_ENABLED = "enabled"
CONF_API_KEY = "Binance API Key"
CONF_API_SECRET = "Binance API Secret"

# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
