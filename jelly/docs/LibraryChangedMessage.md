# LibraryChangedMessage

Library changed message.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**LibraryUpdateInfo**](LibraryUpdateInfo.md) | Gets or sets the data. | [optional] 
**message_id** | **str** | Gets or sets the message id. | [optional] 
**message_type** | [**SessionMessageType**](SessionMessageType.md) | The different kinds of messages that are used in the WebSocket api. | [optional] [readonly] [default to SessionMessageType.LIBRARYCHANGED]

## Example

```python
from openapi_client.models.library_changed_message import LibraryChangedMessage

# TODO update the JSON string below
json = "{}"
# create an instance of LibraryChangedMessage from a JSON string
library_changed_message_instance = LibraryChangedMessage.from_json(json)
# print the JSON string representation of the object
print(LibraryChangedMessage.to_json())

# convert the object into a dict
library_changed_message_dict = library_changed_message_instance.to_dict()
# create an instance of LibraryChangedMessage from a dict
library_changed_message_from_dict = LibraryChangedMessage.from_dict(library_changed_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


