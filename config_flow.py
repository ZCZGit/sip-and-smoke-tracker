from homeassistant import config_entries
import voluptuous as vol
from datetime import datetime
from .const import DOMAIN, CONSUMABLE_TYPES

class SipAndSmokeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Sip and Smoke Tracker."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step: select item type."""
        if user_input is not None:
            # Save the selected item type and proceed to the next step
            self.item_type = user_input["item_type"]
            self._log(f"Selected item type: {self.item_type}")
            return await self.async_step_item_details()

        # Step 1: Ask for the consumable type
        data_schema = vol.Schema({
            vol.Required("item_type"): vol.In(CONSUMABLE_TYPES),
        })
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            description_placeholders={"item_type": "Select a consumable type"},
        )

    async def async_step_item_details(self, user_input=None):
        """Handle the second step: enter item details."""
        if user_input is not None:
            # Auto-generate the entry date
            entry_date = datetime.now().strftime("%Y-%m-%d")
            data = {
                "item_type": self.item_type,
                "item_name": user_input["item_name"],
                "description": user_input.get("description", ""),
                "entry_date": entry_date,
                "image_path": user_input["image_path"],  # Required field
                "amount": user_input.get("amount", 1),  # Default to 1 if not provided
            }

            # Add specific fields for each type
            if self.item_type == "Whisky":
                data.update({
                    "distillery": user_input.get("distillery", ""),
                    "country_of_origin": user_input.get("country_of_origin", ""),
                    "region": user_input.get("region", ""),
                    "age": user_input.get("age", "N/A"),  # Default to N/A
                    "alcohol_type": user_input.get("alcohol_type", ""),
                    "abv": f'{user_input.get("abv", 0)}%',  # Add unit to abv
                })
            elif self.item_type == "Rum":
                data.update({
                    "type": user_input.get("type", ""),
                    "country_of_origin": user_input.get("country_of_origin", ""),
                    "age": user_input.get("age", "N/A"),  # Default to N/A
                    "alcohol_type": user_input.get("alcohol_type", ""),
                    "abv": f'{user_input.get("abv", 0)}%',  # Add unit to abv
                })
            elif self.item_type == "Wine":
                data.update({
                    "type": user_input.get("type", ""),
                    "grapes": user_input.get("grapes", ""),
                    "vintage": user_input.get("vintage", ""),
                    "abv": f'{user_input.get("abv", 0)}%',  # Add unit to abv
                    "country_of_origin": user_input.get("country_of_origin", ""),
                    "region": user_input.get("region", ""),
                    "winery": user_input.get("winery", ""),
                })
            elif self.item_type == "Cigar":
                data.update({
                    "vitola": user_input.get("vitola", ""),
                    "origin": user_input.get("origin", ""),
                    "length": f'{user_input.get("length", 0)}"',  # Add unit to length
                    "burn_time_min": f'{user_input.get("burn_time_min", 0)} min',  # Add unit
                    "burn_time_max": f'{user_input.get("burn_time_max", 0)} min',  # Add unit
                    "strength": user_input.get("strength", ""),
                    "ring_gauge": user_input.get("ring_gauge", ""),
                })
            elif self.item_type == "Coffee":
                data.update({
                    "roastery": user_input.get("roastery", ""),
                    "roast_date": user_input.get("roast_date", ""),
                    "country": user_input.get("country", ""),
                    "region": user_input.get("region", ""),
                    "produced_by": user_input.get("produced_by", ""),
                    "process": user_input.get("process", ""),
                    "variety": user_input.get("variety", ""),
                    "elevation": user_input.get("elevation", ""),
                })

            self._log(f"Creating entry with data: {data}")
            return self.async_create_entry(title=user_input["item_name"], data=data)

        # Base schema includes required fields
        base_schema = {
            vol.Required("item_name"): str,
            vol.Optional("description", default=""): str,
            vol.Required("image_path"): str,  # Required field
            vol.Required("amount"): vol.Coerce(int),  # Required field
        }

        # Add type-specific fields based on the chosen item type
        if self.item_type == "Whisky":
            base_schema.update({
                vol.Optional("distillery", default=""): str,
                vol.Optional("country_of_origin", default=""): str,
                vol.Optional("region", default=""): str,
                vol.Optional("age", default="N/A"): str,
                vol.Optional("alcohol_type", default=""): str,
                vol.Optional("abv", default=0): vol.Coerce(float),
            })
        elif self.item_type == "Rum":
            base_schema.update({
                vol.Optional("type", default=""): str,
                vol.Optional("country_of_origin", default=""): str,
                vol.Optional("age", default="N/A"): str,
                vol.Optional("alcohol_type", default=""): str,
                vol.Optional("abv", default=0): vol.Coerce(float),
            })
        elif self.item_type == "Wine":
            base_schema.update({
                vol.Optional("type", default=""): str,
                vol.Optional("grapes", default=""): str,
                vol.Optional("vintage", default=0): vol.Coerce(int),
                vol.Optional("abv", default=0): vol.Coerce(float),
                vol.Optional("country_of_origin", default=""): str,
                vol.Optional("region", default=""): str,
                vol.Optional("winery", default=""): str,
            })
        elif self.item_type == "Cigar":
            base_schema.update({
                vol.Optional("vitola", default=""): str,
                vol.Optional("origin", default=""): str,
                vol.Optional("length", default=0): vol.Coerce(float),
                vol.Optional("burn_time_min", default=0): vol.Coerce(int),
                vol.Optional("burn_time_max", default=0): vol.Coerce(int),
                vol.Optional("strength", default=""): str,
                vol.Optional("ring_gauge", default=0): vol.Coerce(int),
            })
        elif self.item_type == "Coffee":
            base_schema.update({
                vol.Optional("roastery", default=""): str,
                vol.Optional("roast_date", default="DD/MM/YYYY"): str,
                vol.Optional("country", default=""): str,
                vol.Optional("region", default=""): str,
                vol.Optional("produced_by", default=""): str,
                vol.Optional("process", default=""): str,
                vol.Optional("variety", default=""): str,
                vol.Optional("elevation", default=""): str,
            })

        data_schema = vol.Schema(base_schema)
        self._log(f"Displaying form for item type: {self.item_type}")
        return self.async_show_form(
            step_id="item_details",
            data_schema=data_schema,
        )

    def _log(self, message):
        """Log messages for debugging purposes."""
        print(f"[SipAndSmokeConfigFlow] {message}")

