# UpdateUserItemDataDto

This is used by the api to get information about a item user data.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rating** | **float** | Gets or sets the rating. | [optional] 
**played_percentage** | **float** | Gets or sets the played percentage. | [optional] 
**unplayed_item_count** | **int** | Gets or sets the unplayed item count. | [optional] 
**playback_position_ticks** | **int** | Gets or sets the playback position ticks. | [optional] 
**play_count** | **int** | Gets or sets the play count. | [optional] 
**is_favorite** | **bool** | Gets or sets a value indicating whether this instance is favorite. | [optional] 
**likes** | **bool** | Gets or sets a value indicating whether this MediaBrowser.Model.Dto.UpdateUserItemDataDto is likes. | [optional] 
**last_played_date** | **datetime** | Gets or sets the last played date. | [optional] 
**played** | **bool** | Gets or sets a value indicating whether this MediaBrowser.Model.Dto.UserItemDataDto is played. | [optional] 
**key** | **str** | Gets or sets the key. | [optional] 
**item_id** | **str** | Gets or sets the item identifier. | [optional] 

## Example

```python
from openapi_client.models.update_user_item_data_dto import UpdateUserItemDataDto

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateUserItemDataDto from a JSON string
update_user_item_data_dto_instance = UpdateUserItemDataDto.from_json(json)
# print the JSON string representation of the object
print(UpdateUserItemDataDto.to_json())

# convert the object into a dict
update_user_item_data_dto_dict = update_user_item_data_dto_instance.to_dict()
# create an instance of UpdateUserItemDataDto from a dict
update_user_item_data_dto_from_dict = UpdateUserItemDataDto.from_dict(update_user_item_data_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


