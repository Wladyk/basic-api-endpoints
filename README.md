# basic-api-endpoints

## Deployed: http://wladyk.pythonanywhere.com/

## Authenthication

This app uses JWT auth through djoser. The endpoints related to it are:
_/auth/jwt/users/_ for user creation
_/auth/jwt/create/_ for user validation and auth/refresh token generation
_/auth/jwt/validate/_ for token validation

No user activation is currently enabled.

All protected viewsets should be impacted with the following headers:
_Authorization: JWT <auth_token>_ 

##Exposed endpoints

##### /order/
