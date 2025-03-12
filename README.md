# **Sip and Smoke Tracker - Custom Home Assistant Component**

The **Sip and Smoke Tracker** is a custom Home Assistant component designed to help you manage an inventory of alcoholic beverages, coffees and cigars. This component allows you to keep track of your collection, log attributes like age, origin, flavor profiles, and provide a structured inventory view through sensors.

## **Features**
- **Dynamic Inventory Management**: Automatically track and organize alcohol and cigar collections.
- **Support for Multiple Categories**: Includes Whisky, Rum, Wine, Cigars, and more.
- **Custom Configuration Flow**: Provides an easy setup process with a guided UI in Home Assistant.
- **Entity Creation**: Dynamically creates sensor entities based on inventory data.
- **Home Assistant Native Integration**: Built to work seamlessly with Home Assistant dashboards and automation.
- **Coffee**: Added Coffee as an option to display what is currently in the hopper.

## **Installation**
1. **Add Files**:
   - Add the `sip_and_smoke_tracker` directory into the `custom_components` folder in your Home Assistant configuration directory (`<config>/custom_components/`).
   - Ensure the `custom_components/sip_and_smoke_tracker` folder contains `__init__.py`, `sensor.py`, `config_flow.py`, and other necessary files.

2. **Restart Home Assistant**:
   - Restart Home Assistant to recognize the new custom component.

3. **Add Integration**:
   - Go to **Settings > Devices & Services > Add Integration**.
   - Search for **Sip and Smoke Tracker** and follow the setup flow.

## **Configuration Options**
The integration allows you to define and manage your inventory through the Home Assistant interface. There’s no need to manually edit configuration files.

### **Supported Categories**
The following categories are supported by default:
- **Whisky**
- **Rum**
- **Wine**
- **Cigars**
- **Cigars**

Each category includes fields like **Name**, **Age**, **Origin**, **Flavor Notes**, and more. These fields are dynamically adjustable based on the selected category during the setup process.

## **How It Works**
1. **Setup**:
   - After adding the integration, follow the configuration flow to add inventory items.
   - Select the category (e.g., Whisky, Rum, Wine, or Cigars) and provide the required details.

2. **Entities**:
   - For each inventory item added, sensor entities are created with attributes such as:
     - `name`
     - `origin`
     - `age`
     - `notes`
     - `entry_date`
   - Entities are available for automations, dashboards, or scripts.

3. **Dashboard Integration**:
   - Use the created entities to build custom dashboards, such as a dedicated "Bar & Humidor Inventory" view.

## **Entity Updates**

Entitys in this integration can be permanently changed if required by navigating to:
 - Developer Tools
   - Events
      - Event Type = sip_and_smoke_tracker.update
      - Event Data = entity_id: sensor.IDTOUPDATE
                     value: NEWVALUE
      - Click Fire Event

## **Display Cards**
A custom card to display devices added via this integration.

**[sip-and-smoke-tracker-consumables-card](https://gitea-rpiprd.zcznet.uk/gitchadmin/sip-and-smoke-tracker-consumables-card)**

A custom card which scrapes the `sip-and-smoke-tracker` integration and dynamically populates nested `sip-and-smoke-tracker-consumables-cards` based on consumable type.

**[sip-and-smoke-card](https://gitea-rpiprd.zcznet.uk/gitchadmin/sip-and-smoke-card)**

## **File Overview**

- **`__init__.py`**: Handles the initialization and setup of the integration, including registering platforms and managing lifecycle events.
- **`config_flow.py`**: Provides the configuration flow for adding and managing inventory items.
- **`sensor.py`**: Defines the sensor entities, their attributes, and states.
- **`const.py`**: Contains constants and other shared settings used by the integration.

