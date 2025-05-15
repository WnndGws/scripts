# openapi_client.ClientLogApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**log_file**](ClientLogApi.md#log_file) | **POST** /ClientLog/Document | Upload a document.


# **log_file**
> ClientLogDocumentResponseDto log_file(body=body)

Upload a document.

### Example

* Api Key Authentication (CustomAuthentication):

```python
import openapi_client
from openapi_client.models.client_log_document_response_dto import ClientLogDocumentResponseDto
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: CustomAuthentication
configuration.api_key['CustomAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['CustomAuthentication'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ClientLogApi(api_client)
    body = None # bytearray |  (optional)

    try:
        # Upload a document.
        api_response = api_instance.log_file(body=body)
        print("The response of ClientLogApi->log_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ClientLogApi->log_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **bytearray**|  | [optional] 

### Return type

[**ClientLogDocumentResponseDto**](ClientLogDocumentResponseDto.md)

### Authorization

[CustomAuthentication](../README.md#CustomAuthentication)

### HTTP request headers

 - **Content-Type**: text/plain
 - **Accept**: application/json, application/json; profile="CamelCase", application/json; profile="PascalCase"

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Document saved. |  -  |
**401** | Unauthorized |  -  |
**403** | Event logging disabled. |  -  |
**413** | Upload size too large. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

