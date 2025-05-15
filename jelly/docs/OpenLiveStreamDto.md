# OpenLiveStreamDto

Open live stream dto.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**open_token** | **str** | Gets or sets the open token. | [optional] 
**user_id** | **str** | Gets or sets the user id. | [optional] 
**play_session_id** | **str** | Gets or sets the play session id. | [optional] 
**max_streaming_bitrate** | **int** | Gets or sets the max streaming bitrate. | [optional] 
**start_time_ticks** | **int** | Gets or sets the start time in ticks. | [optional] 
**audio_stream_index** | **int** | Gets or sets the audio stream index. | [optional] 
**subtitle_stream_index** | **int** | Gets or sets the subtitle stream index. | [optional] 
**max_audio_channels** | **int** | Gets or sets the max audio channels. | [optional] 
**item_id** | **str** | Gets or sets the item id. | [optional] 
**enable_direct_play** | **bool** | Gets or sets a value indicating whether to enable direct play. | [optional] 
**enable_direct_stream** | **bool** | Gets or sets a value indicating whether to enale direct stream. | [optional] 
**always_burn_in_subtitle_when_transcoding** | **bool** | Gets or sets a value indicating whether always burn in subtitles when transcoding. | [optional] 
**device_profile** | [**DeviceProfile**](DeviceProfile.md) | A MediaBrowser.Model.Dlna.DeviceProfile represents a set of metadata which determines which content a certain device is able to play.  &lt;br /&gt;  Specifically, it defines the supported &lt;see cref&#x3D;\&quot;P:MediaBrowser.Model.Dlna.DeviceProfile.ContainerProfiles\&quot;&gt;containers&lt;/see&gt; and  &lt;see cref&#x3D;\&quot;P:MediaBrowser.Model.Dlna.DeviceProfile.CodecProfiles\&quot;&gt;codecs&lt;/see&gt; (video and/or audio, including codec profiles and levels)  the device is able to direct play (without transcoding or remuxing),  as well as which &lt;see cref&#x3D;\&quot;P:MediaBrowser.Model.Dlna.DeviceProfile.TranscodingProfiles\&quot;&gt;containers/codecs to transcode to&lt;/see&gt; in case it isn&#39;t. | [optional] 
**direct_play_protocols** | [**List[MediaProtocol]**](MediaProtocol.md) | Gets or sets the device play protocols. | [optional] 

## Example

```python
from openapi_client.models.open_live_stream_dto import OpenLiveStreamDto

# TODO update the JSON string below
json = "{}"
# create an instance of OpenLiveStreamDto from a JSON string
open_live_stream_dto_instance = OpenLiveStreamDto.from_json(json)
# print the JSON string representation of the object
print(OpenLiveStreamDto.to_json())

# convert the object into a dict
open_live_stream_dto_dict = open_live_stream_dto_instance.to_dict()
# create an instance of OpenLiveStreamDto from a dict
open_live_stream_dto_from_dict = OpenLiveStreamDto.from_dict(open_live_stream_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


