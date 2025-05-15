# openapi_client.BrandingApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_branding_css**](BrandingApi.md#get_branding_css) | **GET** /Branding/Css | Gets branding css.
[**get_branding_css2**](BrandingApi.md#get_branding_css2) | **GET** /Branding/Css.css | Gets branding css.
[**get_branding_options**](BrandingApi.md#get_branding_options) | **GET** /Branding/Configuration | Gets branding configuration.


# **get_branding_css**
> str get_branding_css()

Gets branding css.

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
    api_instance = openapi_client.BrandingApi(api_client)

    try:
        # Gets branding css.
        api_response = api_instance.get_branding_css()
        print("The response of BrandingApi->get_branding_css:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrandingApi->get_branding_css: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/css, application/json, application/json; profile="CamelCase", application/json; profile="PascalCase"

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Branding css returned. |  -  |
**204** | No branding css configured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_branding_css2**
> str get_branding_css2()

Gets branding css.

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
    api_instance = openapi_client.BrandingApi(api_client)

    try:
        # Gets branding css.
        api_response = api_instance.get_branding_css2()
        print("The response of BrandingApi->get_branding_css2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrandingApi->get_branding_css2: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/css, application/json, application/json; profile="CamelCase", application/json; profile="PascalCase"

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Branding css returned. |  -  |
**204** | No branding css configured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_branding_options**
> BrandingOptions get_branding_options()

Gets branding configuration.

### Example


```python
import openapi_client
from openapi_client.models.branding_options import BrandingOptions
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
    api_instance = openapi_client.BrandingApi(api_client)

    try:
        # Gets branding configuration.
        api_response = api_instance.get_branding_options()
        print("The response of BrandingApi->get_branding_options:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrandingApi->get_branding_options: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**BrandingOptions**](BrandingOptions.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/json; profile="CamelCase", application/json; profile="PascalCase"

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Branding configuration returned. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

