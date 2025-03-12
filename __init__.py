import logging
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry):
    """Set up Sip and Smoke Tracker from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Prevent duplicate setup of the same entry
    if config_entry.entry_id in hass.data[DOMAIN]:
        _LOGGER.warning("Config entry %s is already set up!", config_entry.entry_id)
        return False

    hass.data[DOMAIN][config_entry.entry_id] = config_entry.data

    # Forward the entry to the sensor platform for entity creation
    await hass.config_entries.async_forward_entry_setups(config_entry, ["sensor"])
    _LOGGER.info("Successfully set up config entry %s for Sip and Smoke Tracker.", config_entry.entry_id)
    return True

async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    if config_entry.entry_id not in hass.data[DOMAIN]:
        _LOGGER.warning("Config entry %s is not found in active data.", config_entry.entry_id)
        return False

    # Remove entry from hass data
    hass.data[DOMAIN].pop(config_entry.entry_id)

    # Unload the sensor platform for the entry
    unload_ok = await hass.config_entries.async_forward_entry_unload(config_entry, "sensor")
    if unload_ok:
        _LOGGER.info("Successfully unloaded config entry %s for Sip and Smoke Tracker.", config_entry.entry_id)
    else:
        _LOGGER.error("Failed to unload config entry %s.", config_entry.entry_id)

    return unload_ok

