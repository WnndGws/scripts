# openapi_client.VideoAttachmentsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_attachment**](VideoAttachmentsApi.md#get_attachment) | **GET** /Videos/{videoId}/{mediaSourceId}/Attachments/{index} | Get video attachment.


# **get_attachment**
> bytearray get_attachment(video_id, media_source_id, index)

Get video attachment.

### Example


```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.VideoAttachmentsApi(api_client)
    video_id = 'video_id_example' # str | Video ID.
    media_source_id = 'media_source_id_example' # str | Media Source ID.
    index = 56 # int | Attachment Index.

    try:
        # Get video attachment.
        api_response = api_instance.get_attachment(video_id, media_source_id, index)
        print("The response of VideoAttachmentsApi->get_attachment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VideoAttachmentsApi->get_attachment: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **video_id** | **str**| Video ID. | 
 **media_source_id** | **str**| Media Source ID. | 
 **index** | **int**| Attachment Index. | 

### Return type

**bytearray**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream, application/json, application/json; profile="CamelCase", application/json; profile="PascalCase"

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Attachment retrieved. |  -  |
**404** | Video or attachment not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

