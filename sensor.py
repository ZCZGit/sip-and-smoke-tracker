from homeassistant.helpers.entity import Entity
from homeassistant.helpers.device_registry import async_get
from .const import DOMAIN
import logging
import random

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up consumable entities for this config entry."""
    data = config_entry.data

    # Register a device for the consumable
    device_registry = async_get(hass)
    device = device_registry.async_get_or_create(
        config_entry_id=config_entry.entry_id,
        identifiers={(DOMAIN, config_entry.entry_id)},
        manufacturer="Sip and Smoke Tracker",
        name=data["item_name"],
        model=data["item_type"],  # E.g., whisky, rum, wine, cigar
    )

    # Dynamically create entities for all attributes in config_entry.data
    entities = []

    # Explicitly create entities for mandatory fields
    entities.append(ConsumableEntity(data["item_name"], "Name", data["item_name"], config_entry, device.id))
    entities.append(ConsumableEntity(data["item_name"], "Description", data.get("description", ""), config_entry, device.id))
    entities.append(ConsumableEntity(data["item_name"], "Image Path", data.get("image_path", ""), config_entry, device.id))
    entities.append(ConsumableEntity(data["item_name"], "Entry Date", data.get("entry_date", ""), config_entry, device.id))  # Add the entry_date entity

    # Dynamically add entities for all other fields
    for key, value in data.items():
        if key in ["item_name", "item_type", "description", "entry_date", "image_path"]:
            continue  # Skip fields already handled above
        entities.append(ConsumableEntity(data["item_name"], key, value, config_entry, device.id))

    async_add_entities(entities)

    # Listen for custom events to trigger async_update
    async def handle_update_event(event):
        """Handle the custom update event to trigger async_update."""
        entity_id = event.data.get("entity_id")
        value = event.data.get("value")  # Get the specified value from the event data

        for entity in entities:
            if entity.entity_id == entity_id:
                _LOGGER.info("Custom event triggered for %s with value: %s. Updating state.", entity_id, value)

                # Update the entity state
                await entity.async_update(value=value)

                # Persist the updated value in the config entry
                entity_name = entity._item_name  # Extract the item name
                parameter = entity._parameter.lower()

                new_data = dict(entity._config_entry.data)
                new_data[parameter] = value  # Update the specific parameter in config_entry.data

                hass.config_entries.async_update_entry(
                    entity._config_entry, data=new_data
                )
                _LOGGER.info("Persisted %s: %s to config_entry.", parameter, value)
                break
        else:
            _LOGGER.warning("No matching entity found for event: %s", event.data)

    # Register the event listener
    hass.bus.async_listen("sip_and_smoke_tracker.update", handle_update_event)


class ConsumableEntity(Entity):
    """Representation of a consumable parameter."""

    def __init__(self, item_name, parameter, value, config_entry, device_id):
        """Initialize the consumable parameter entity."""
        self._item_name = item_name
        self._parameter = parameter
        self._value = value
        self._config_entry = config_entry
        self._device_id = device_id
        self._unique_id = f"{config_entry.entry_id}_{parameter.lower()}"

    @property
    def unique_id(self):
        """Return a unique ID for the entity."""
        return self._unique_id

    @property
    def name(self):
        """Return the name of the entity."""
        # Name format: "<item_name> <parameter>" (e.g., "Glenlivet 18 ABV")
        return f"{self._item_name} {self._parameter.replace('_', ' ').title()}"

    @property
    def state(self):
        """Return the state of the entity."""
        return self._value

    @property
    def extra_state_attributes(self):
        """Return additional attributes for the entity."""
        attributes = {"device_id": self._device_id}

        if self._parameter.lower() == "image path":
            attributes["image_url"] = self._value  # Add an explicit image URL attribute

        return attributes

    @property
    def device_info(self):
        """Return device info for this entity."""
        return {
            "identifiers": {(DOMAIN, self._config_entry.entry_id)},
            "name": self._item_name,
            "manufacturer": "Sip and Smoke Tracker",
            "model": self._config_entry.data["item_type"],
        }

    async def async_update(self, value=None):
        """Fetch new data for the entity, using the provided value if available."""
        if value is not None:
            # Use the value provided in the event
            self._value = value
            _LOGGER.info("Updated %s to specified value: %s", self.name, self._value)
        else:
            _LOGGER.debug("No value provided for update; state remains unchanged.")

        # Notify Home Assistant of the state change
        self.async_write_ha_state()

