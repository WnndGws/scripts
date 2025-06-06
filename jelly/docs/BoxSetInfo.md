# BoxSetInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Gets or sets the name. | [optional] 
**original_title** | **str** | Gets or sets the original title. | [optional] 
**path** | **str** | Gets or sets the path. | [optional] 
**metadata_language** | **str** | Gets or sets the metadata language. | [optional] 
**metadata_country_code** | **str** | Gets or sets the metadata country code. | [optional] 
**provider_ids** | **Dict[str, Optional[str]]** | Gets or sets the provider ids. | [optional] 
**year** | **int** | Gets or sets the year. | [optional] 
**index_number** | **int** |  | [optional] 
**parent_index_number** | **int** |  | [optional] 
**premiere_date** | **datetime** |  | [optional] 
**is_automated** | **bool** |  | [optional] 

## Example

```python
from openapi_client.models.box_set_info import BoxSetInfo

# TODO update the JSON string below
json = "{}"
# create an instance of BoxSetInfo from a JSON string
box_set_info_instance = BoxSetInfo.from_json(json)
# print the JSON string representation of the object
print(BoxSetInfo.to_json())

# convert the object into a dict
box_set_info_dict = box_set_info_instance.to_dict()
# create an instance of BoxSetInfo from a dict
box_set_info_from_dict = BoxSetInfo.from_dict(box_set_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


