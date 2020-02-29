from enum import Enum


class MerossEventType(Enum):
    # Fired when the MQTT client connects/disconnects to the MQTT broker
    CLIENT_CONNECTION = 10
    DEVICE_ONLINE_STATUS = 100
    DEVICE_BIND = 200
    DEVICE_UNBIND = 201
    DEVICE_SWITCH_STATUS = 1000
    DEVICE_BULB_SWITCH_STATE = 2000
    DEVICE_BULB_STATE = 2001
    GARAGE_DOOR_STATUS = 3000
    THERMOSTAT_TEMPERATURE_CHANGE = 5000
    THERMOSTAT_MODE_CHANGE = 5001
    HUMIDIFIER_SPRY_EVENT = 6000
    HUMIDIFIER_LIGHT_EVENT = 6001


class MerossEvent(object):
    event_type = None  # type: MerossEventType

    def __init__(self, event_type):
        self.event_type = event_type


class DeviceBindEvent(MerossEvent):
    def __init__(self, device, bind_data):
        super(DeviceBindEvent, self).__init__(MerossEventType.DEVICE_BIND)
        self.device = device
        self.bind_data = bind_data


class DeviceUnbindEvent(MerossEvent):
    def __init__(self, device):
        super(DeviceUnbindEvent, self).__init__(MerossEventType.DEVICE_UNBIND)
        self.device = device


class ClientConnectionEvent(MerossEvent):
    status = None

    def __init__(self, current_status):
        super(ClientConnectionEvent, self).__init__(MerossEventType.CLIENT_CONNECTION)
        self.status = current_status


class DeviceOnlineStatusEvent(MerossEvent):
    # Pointer to the device object
    device = None

    # Current status of the device
    status = None

    def __init__(self, dev, current_status):
        super(DeviceOnlineStatusEvent, self).__init__(MerossEventType.DEVICE_ONLINE_STATUS)
        self.device = dev
        self.status = "online" if current_status else "offline"


class DeviceSwitchStatusEvent(MerossEvent):
    # Pointer to the device object
    device = None

    # Channel ID where the event occurred
    channel_id = None

    # Current state of the switch where the event occurred
    switch_state = None

    # Indicates id the event was generated by a command issued by the library itself.
    # This is particularly useful in the case the user handler wants only to react
    # to events generated by third parties.
    generated_by_myself = None

    def __init__(self, dev, channel_id, switch_state, generated_by_myself):
        super(DeviceSwitchStatusEvent, self).__init__(MerossEventType.DEVICE_SWITCH_STATUS)
        self.device = dev
        self.channel_id = channel_id
        self.switch_state = switch_state
        self.generated_by_myself = generated_by_myself


class DeviceDoorStatusEvent(MerossEvent):
    # Pointer to the device object
    device = None

    # Current state of the door
    door_state = None

    # Channel related to the door controller
    channel = None

    # Indicates id the event was generated by a command issued by the library itself.
    # This is particularly useful in the case the user handler wants only to react
    # to events generated by third parties.
    generated_by_myself = None

    def __init__(self, dev, channel_id, door_state, generated_by_myself):
        super(DeviceDoorStatusEvent, self).__init__(MerossEventType.GARAGE_DOOR_STATUS)
        self.device = dev
        self.channel = channel_id
        self.door_state = "open" if door_state else "closed"
        self.generated_by_myself = generated_by_myself


class BulbSwitchStateChangeEvent(MerossEvent):
    def __init__(self, dev, channel_id, is_on, generated_by_myself):
        super(BulbSwitchStateChangeEvent, self).__init__(MerossEventType.DEVICE_BULB_SWITCH_STATE)
        self.device = dev
        self.channel = channel_id
        self.is_on = is_on
        self.generated_by_myself = generated_by_myself


class BulbLightStateChangeEvent(MerossEvent):
    def __init__(self, dev, channel_id, light_state, generated_by_myself):
        super(BulbLightStateChangeEvent, self).__init__(MerossEventType.DEVICE_BULB_STATE)
        self.device = dev
        self.channel = channel_id
        self.light_state = light_state
        self.generated_by_myself = generated_by_myself


class ThermostatTemperatureChange(MerossEvent):
    def __init__(self, device, temperature_state, generated_by_myself):
        super(ThermostatTemperatureChange, self).__init__(MerossEventType.THERMOSTAT_TEMPERATURE_CHANGE)
        self.device = device
        self.temperature = temperature_state
        self.generated_by_myself = generated_by_myself


class ThermostatModeChange(MerossEvent):
    def __init__(self, device, mode, generated_by_myself):
        super(ThermostatModeChange, self).__init__(MerossEventType.THERMOSTAT_MODE_CHANGE)
        self.device = device
        self.mode = mode
        self.generated_by_myself = generated_by_myself


class HumidifierSpryEvent(MerossEvent):
    def __init__(self, device, spry_mode, channel, generated_by_myself):
        super(HumidifierSpryEvent, self).__init__(MerossEventType.HUMIDIFIER_SPRY_EVENT)
        self.device = device
        self.spry_mode = spry_mode
        self.channel = channel
        self.generated_by_myself = generated_by_myself


class HumidifierLightEvent(MerossEvent):
    def __init__(self, dev, channel, onoff, rgb, luminance, generated_by_myself):
        super(HumidifierLightEvent, self).__init__(MerossEventType.HUMIDIFIER_LIGHT_EVENT)
        self.device = dev
        self.channel = channel
        self.is_on = onoff == 1
        self.rgb = rgb
        self.luminance = luminance
        self.generated_by_myself = generated_by_myself