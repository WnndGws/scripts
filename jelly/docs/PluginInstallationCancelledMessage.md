# PluginInstallationCancelledMessage

Plugin installation cancelled message.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**InstallationInfo**](InstallationInfo.md) | Gets or sets the data. | [optional] 
**message_id** | **str** | Gets or sets the message id. | [optional] 
**message_type** | [**SessionMessageType**](SessionMessageType.md) | The different kinds of messages that are used in the WebSocket api. | [optional] [readonly] [default to SessionMessageType.PACKAGEINSTALLATIONCANCELLED]

## Example

```python
from openapi_client.models.plugin_installation_cancelled_message import PluginInstallationCancelledMessage

# TODO update the JSON string below
json = "{}"
# create an instance of PluginInstallationCancelledMessage from a JSON string
plugin_installation_cancelled_message_instance = PluginInstallationCancelledMessage.from_json(json)
# print the JSON string representation of the object
print(PluginInstallationCancelledMessage.to_json())

# convert the object into a dict
plugin_installation_cancelled_message_dict = plugin_installation_cancelled_message_instance.to_dict()
# create an instance of PluginInstallationCancelledMessage from a dict
plugin_installation_cancelled_message_from_dict = PluginInstallationCancelledMessage.from_dict(plugin_installation_cancelled_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


