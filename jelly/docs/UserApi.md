# openapi_client.UserApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**authenticate_user_by_name**](UserApi.md#authenticate_user_by_name) | **POST** /Users/AuthenticateByName | Authenticates a user by name.
[**authenticate_with_quick_connect**](UserApi.md#authenticate_with_quick_connect) | **POST** /Users/AuthenticateWithQuickConnect | Authenticates a user with quick connect.
[**create_user_by_name**](UserApi.md#create_user_by_name) | **POST** /Users/New | Creates a user.
[**delete_user**](UserApi.md#delete_user) | **DELETE** /Users/{userId} | Deletes a user.
[**forgot_password**](UserApi.md#forgot_password) | **POST** /Users/ForgotPassword | Initiates the forgot password process for a local user.
[**forgot_password_pin**](UserApi.md#forgot_password_pin) | **POST** /Users/ForgotPassword/Pin | Redeems a forgot password pin.
[**get_current_user**](UserApi.md#get_current_user) | **GET** /Users/Me | Gets the user based on auth token.
[**get_public_users**](UserApi.md#get_public_users) | **GET** /Users/Public | Gets a list of publicly visible users for display on a login screen.
[**get_user_by_id**](UserApi.md#get_user_by_id) | **GET** /Users/{userId} | Gets a user by Id.
[**get_users**](UserApi.md#get_users) | **GET** /Users | Gets a list of users.
[**update_user**](UserApi.md#update_user) | **POST** /Users | Updates a user.
[**update_user_configuration**](UserApi.md#update_user_configuration) | **POST** /Users/Configuration | Updates a user configuration.
[**update_user_password**](UserApi.md#update_user_password) | **POST** /Users/Password | Updates a user&#39;s password.
[**update_user_policy**](UserApi.md#update_user_policy) | **POST** /Users/{userId}/Policy | Updates a user policy.


# **authenticate_user_by_name**
> AuthenticationResult authenticate_user_by_name(authenticate_user_by_name)

Authenticates a user by name.

### Example


```python
import openapi_client
from openapi_client.models.authenticate_user_by_name import AuthenticateUserByName
from openapi_client.models.authentication_result import AuthenticationResult
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
    api_instance = openapi_client.UserApi(api_client)
    authenticate_user_by_name = openapi_client.AuthenticateUserByName() # AuthenticateUserByName | The M:Jellyfin.Api.Controllers.UserController.AuthenticateUserByName(Jellyfin.Api.Models.UserDtos.AuthenticateUserByName) request.

    try:
        # Authenticates a user by name.
        api_response = api_instance.authenticate_user_by_name(authenticate_user_by_name)
        print("The response of UserApi->authenticate_user_by_name:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->authenticate_user_by_name: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authenticate_user_by_name** | [**AuthenticateUserByName**](AuthenticateUserByName.md)| The M:Jellyfin.Api.Controllers.UserController.AuthenticateUserByName(Jellyfin.Api.Models.UserDtos.AuthenticateUserByName) request. | 

### Return type

[**AuthenticationResult**](AuthenticationResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, text/json, application/*+json
 - **Accept**: application/json, application/json; profile="CamelCase", application/json; profile="PascalCase"

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User authenticated. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **authenticate_with_quick_connect**
> AuthenticationResult authenticate_with_quick_connect(quick_connect_dto)

Authenticates a user with quick connect.

### Example


```python
import openapi_client
from openapi_client.models.authentication_result import AuthenticationResult
from openapi_client.models.quick_connect_dto import QuickConnectDto
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
    api_instance = openapi_client.UserApi(api_client)
    quick_connect_dto = openapi_client.QuickConnectDto() # QuickConnectDto | The Jellyfin.Api.Models.UserDtos.QuickConnectDto request.

    try:
        # Authenticates a user with quick connect.
        api_response = api_instance.authenticate_with_quick_connect(quick_connect_dto)
        print("The response of UserApi->authenticate_with_quick_connect:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->authenticate_with_quick_connect: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **quick_connect_dto** | [**QuickConnectDto**](QuickConnectDto.md)| The Jellyfin.Api.Models.UserDtos.QuickConnectDto request. | 

### Return type

[**AuthenticationResult**](AuthenticationResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, text/json, application/*+json
 - **Accept**: application/json, application/json; profile="CamelCase", application/json; profile="PascalCase"

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User authenticated. |  -  |
**400** | Missing token. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_user_by_name**
> UserDto create_user_by_name(create_user_by_name)

Creates a user.

### Example

* Api Key Authentication (CustomAuthentication):

```python
import openapi_client
from openapi_client.models.create_user_by_name import CreateUserByName
from openapi_client.models.user_dto import UserDto
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
    api_instance = openapi_client.UserApi(api_client)
    create_user_by_name = openapi_client.CreateUserByName() # CreateUserByName | The create user by name request body.

    try:
        # Creates a user.
        api_response = api_instance.create_user_by_name(create_user_by_name)
        print("The response of UserApi->create_user_by_name:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->create_user_by_name: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_user_by_name** | [**CreateUserByName**](CreateUserByName.md)| The create user by name request body. | 

### Return type

[**UserDto**](UserDto.md)

### Authorization

[CustomAuthentication](../README.md#CustomAuthentication)

### HTTP request headers

 - **Content-Type**: application/json, text/json, application/*+json
 - **Accept**: application/json, application/json; profile="CamelCase", application/json; profile="PascalCase"

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User created. |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_user**
> delete_user(user_id)

Deletes a user.

### Example

* Api Key Authentication (CustomAuthentication):

```python
import openapi_client
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
    api_instance = openapi_client.UserApi(api_client)
    user_id = 'user_id_example' # str | The user id.

    try:
        # Deletes a user.
        api_instance.delete_user(user_id)
    except Exception as e:
        print("Exception when calling UserApi->delete_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| The user id. | 

### Return type

void (empty response body)

### Authorization

[CustomAuthentication](../README.md#CustomAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/json; profile="CamelCase", application/json; profile="PascalCase"

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | User deleted. |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | User not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **forgot_password**
> ForgotPasswordResult forgot_password(forgot_password_dto)

Initiates the forgot password process for a local user.

### Example


```python
import openapi_client
from openapi_client.models.forgot_password_dto import ForgotPasswordDto
from openapi_client.models.forgot_password_result import ForgotPasswordResult
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
    api_instance = openapi_client.UserApi(api_client)
    forgot_password_dto = openapi_client.ForgotPasswordDto() # ForgotPasswordDto | The forgot password request containing the entered username.

    try:
        # Initiates the forgot password process for a local user.
        api_response = api_instance.forgot_password(forgot_password_dto)
        print("The response of UserApi->forgot_password:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->forgot_password: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **forgot_password_dto** | [**ForgotPasswordDto**](ForgotPasswordDto.md)| The forgot password request containing the entered username. | 

### Return type

[**ForgotPasswordResult**](ForgotPasswordResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, text/json, application/*+json
 - **Accept**: application/json, application/json; profile="CamelCase", application/json; profile="PascalCase"

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Password reset process started. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **forgot_password_pin**
> PinRedeemResult forgot_password_pin(forgot_password_pin_dto)

Redeems a forgot password pin.

### Example


```python
import openapi_client
from openapi_client.models.forgot_password_pin_dto import ForgotPasswordPinDto
from openapi_client.models.pin_redeem_result import PinRedeemResult
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
    api_instance = openapi_client.UserApi(api_client)
    forgot_password_pin_dto = openapi_client.ForgotPasswordPinDto() # ForgotPasswordPinDto | The forgot password pin request containing the entered pin.

    try:
        # Redeems a forgot password pin.
        api_response = api_instance.forgot_password_pin(forgot_password_pin_dto)
        print("The response of UserApi->forgot_password_pin:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->forgot_password_pin: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **forgot_password_pin_dto** | [**ForgotPasswordPinDto**](ForgotPasswordPinDto.md)| The forgot password pin request containing the entered pin. | 

### Return type

[**PinRedeemResult**](PinRedeemResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, text/json, application/*+json
 - **Accept**: application/json, application/json; profile="CamelCase", application/json; profile="PascalCase"

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Pin reset process started. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_current_user**
> UserDto get_current_user()

Gets the user based on auth token.

### Example

* Api Key Authentication (CustomAuthentication):

```python
import openapi_client
from openapi_client.models.user_dto import UserDto
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
    api_instance = openapi_client.UserApi(api_client)

    try:
        # Gets the user based on auth token.
        api_response = api_instance.get_current_user()
        print("The response of UserApi->get_current_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->get_current_user: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**UserDto**](UserDto.md)

### Authorization

[CustomAuthentication](../README.md#CustomAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/json; profile="CamelCase", application/json; profile="PascalCase"

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User returned. |  -  |
**400** | Token is not owned by a user. |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_public_users**
> List[UserDto] get_public_users()

Gets a list of publicly visible users for display on a login screen.

### Example


```python
import openapi_client
from openapi_client.models.user_dto import UserDto
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
    api_instance = openapi_client.UserApi(api_client)

    try:
        # Gets a list of publicly visible users for display on a login screen.
        api_response = api_instance.get_public_users()
        print("The response of UserApi->get_public_users:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->get_public_users: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[UserDto]**](UserDto.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/json; profile="CamelCase", application/json; profile="PascalCase"

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Public users returned. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_by_id**
> UserDto get_user_by_id(user_id)

Gets a user by Id.

### Example

* Api Key Authentication (CustomAuthentication):

```python
import openapi_client
from openapi_client.models.user_dto import UserDto
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
    api_instance = openapi_client.UserApi(api_client)
    user_id = 'user_id_example' # str | The user id.

    try:
        # Gets a user by Id.
        api_response = api_instance.get_user_by_id(user_id)
        print("The response of UserApi->get_user_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->get_user_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| The user id. | 

### Return type

[**UserDto**](UserDto.md)

### Authorization

[CustomAuthentication](../README.md#CustomAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/json; profile="CamelCase", application/json; profile="PascalCase"

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User returned. |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | User not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_users**
> List[UserDto] get_users(is_hidden=is_hidden, is_disabled=is_disabled)

Gets a list of users.

### Example

* Api Key Authentication (CustomAuthentication):

```python
import openapi_client
from openapi_client.models.user_dto import UserDto
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
    api_instance = openapi_client.UserApi(api_client)
    is_hidden = True # bool | Optional filter by IsHidden=true or false. (optional)
    is_disabled = True # bool | Optional filter by IsDisabled=true or false. (optional)

    try:
        # Gets a list of users.
        api_response = api_instance.get_users(is_hidden=is_hidden, is_disabled=is_disabled)
        print("The response of UserApi->get_users:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->get_users: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **is_hidden** | **bool**| Optional filter by IsHidden&#x3D;true or false. | [optional] 
 **is_disabled** | **bool**| Optional filter by IsDisabled&#x3D;true or false. | [optional] 

### Return type

[**List[UserDto]**](UserDto.md)

### Authorization

[CustomAuthentication](../README.md#CustomAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/json; profile="CamelCase", application/json; profile="PascalCase"

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Users returned. |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user**
> update_user(user_dto, user_id=user_id)

Updates a user.

### Example

* Api Key Authentication (CustomAuthentication):

```python
import openapi_client
from openapi_client.models.user_dto import UserDto
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
    api_instance = openapi_client.UserApi(api_client)
    user_dto = openapi_client.UserDto() # UserDto | The updated user model.
    user_id = 'user_id_example' # str | The user id. (optional)

    try:
        # Updates a user.
        api_instance.update_user(user_dto, user_id=user_id)
    except Exception as e:
        print("Exception when calling UserApi->update_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_dto** | [**UserDto**](UserDto.md)| The updated user model. | 
 **user_id** | **str**| The user id. | [optional] 

### Return type

void (empty response body)

### Authorization

[CustomAuthentication](../README.md#CustomAuthentication)

### HTTP request headers

 - **Content-Type**: application/json, text/json, application/*+json
 - **Accept**: application/json, application/json; profile="CamelCase", application/json; profile="PascalCase"

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | User updated. |  -  |
**400** | User information was not supplied. |  -  |
**401** | Unauthorized |  -  |
**403** | User update forbidden. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user_configuration**
> update_user_configuration(user_configuration, user_id=user_id)

Updates a user configuration.

### Example

* Api Key Authentication (CustomAuthentication):

```python
import openapi_client
from openapi_client.models.user_configuration import UserConfiguration
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
    api_instance = openapi_client.UserApi(api_client)
    user_configuration = openapi_client.UserConfiguration() # UserConfiguration | The new user configuration.
    user_id = 'user_id_example' # str | The user id. (optional)

    try:
        # Updates a user configuration.
        api_instance.update_user_configuration(user_configuration, user_id=user_id)
    except Exception as e:
        print("Exception when calling UserApi->update_user_configuration: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_configuration** | [**UserConfiguration**](UserConfiguration.md)| The new user configuration. | 
 **user_id** | **str**| The user id. | [optional] 

### Return type

void (empty response body)

### Authorization

[CustomAuthentication](../README.md#CustomAuthentication)

### HTTP request headers

 - **Content-Type**: application/json, text/json, application/*+json
 - **Accept**: application/json, application/json; profile="CamelCase", application/json; profile="PascalCase"

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | User configuration updated. |  -  |
**401** | Unauthorized |  -  |
**403** | User configuration update forbidden. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user_password**
> update_user_password(update_user_password, user_id=user_id)

Updates a user's password.

### Example

* Api Key Authentication (CustomAuthentication):

```python
import openapi_client
from openapi_client.models.update_user_password import UpdateUserPassword
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
    api_instance = openapi_client.UserApi(api_client)
    update_user_password = openapi_client.UpdateUserPassword() # UpdateUserPassword | The M:Jellyfin.Api.Controllers.UserController.UpdateUserPassword(System.Nullable{System.Guid},Jellyfin.Api.Models.UserDtos.UpdateUserPassword) request.
    user_id = 'user_id_example' # str | The user id. (optional)

    try:
        # Updates a user's password.
        api_instance.update_user_password(update_user_password, user_id=user_id)
    except Exception as e:
        print("Exception when calling UserApi->update_user_password: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **update_user_password** | [**UpdateUserPassword**](UpdateUserPassword.md)| The M:Jellyfin.Api.Controllers.UserController.UpdateUserPassword(System.Nullable{System.Guid},Jellyfin.Api.Models.UserDtos.UpdateUserPassword) request. | 
 **user_id** | **str**| The user id. | [optional] 

### Return type

void (empty response body)

### Authorization

[CustomAuthentication](../README.md#CustomAuthentication)

### HTTP request headers

 - **Content-Type**: application/json, text/json, application/*+json
 - **Accept**: application/json, application/json; profile="CamelCase", application/json; profile="PascalCase"

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Password successfully reset. |  -  |
**401** | Unauthorized |  -  |
**403** | User is not allowed to update the password. |  -  |
**404** | User not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user_policy**
> update_user_policy(user_id, user_policy)

Updates a user policy.

### Example

* Api Key Authentication (CustomAuthentication):

```python
import openapi_client
from openapi_client.models.user_policy import UserPolicy
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
    api_instance = openapi_client.UserApi(api_client)
    user_id = 'user_id_example' # str | The user id.
    user_policy = openapi_client.UserPolicy() # UserPolicy | The new user policy.

    try:
        # Updates a user policy.
        api_instance.update_user_policy(user_id, user_policy)
    except Exception as e:
        print("Exception when calling UserApi->update_user_policy: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| The user id. | 
 **user_policy** | [**UserPolicy**](UserPolicy.md)| The new user policy. | 

### Return type

void (empty response body)

### Authorization

[CustomAuthentication](../README.md#CustomAuthentication)

### HTTP request headers

 - **Content-Type**: application/json, text/json, application/*+json
 - **Accept**: application/json, application/json; profile="CamelCase", application/json; profile="PascalCase"

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | User policy updated. |  -  |
**400** | User policy was not supplied. |  -  |
**401** | Unauthorized |  -  |
**403** | User policy update forbidden. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

