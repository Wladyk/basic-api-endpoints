# basic-api-endpoints

## Deployed: http://wladyk.pythonanywhere.com/

## Authenthication

This app uses JWT auth through djoser. The endpoints related to it are:
_/auth/jwt/users/_ for user creation. 

_/auth/jwt/create/_ for user validation and auth/refresh token generation.

_/auth/jwt/validate/_ for token validation.


No user activation is currently enabled.

All protected viewsets should be impacted with the following headers:
_Authorization: JWT <auth_token>_ 

## Exposed endpoints

#### /order/
JWT protected.


Method GET: provides Orders list, including their details.

#### /order/key
Method GET: provides order detail.__
Method POST: listens for JSON payload to create a new order. Expected payload syntax:
```
{ "date_time": "2020-01-01 20:00:00",
   "details": [
          {"productId": "ac334",
           "quantity" : 10,
          },
          {"productId": "t01",
           "quantity": 10,
          }
    ]
  }
```
Method PUT: Listens for JSON payload to update an existing order or its details. If a new product is added to the details, it will be added to the order. Expected payload syntax: 
```
{ "date_time": "2020-01-01 20:00:00",
   "details": [
          {"productId": "ac334",
           "quantity" : 10,
          },
          {"productId": "t01",
           "quantity": 10,
          }
    ]
  }
```
Method DELETE: Destroys the given order and all its related details.

#### /order/key/deleteProduct
Method POST: Deletes a given product from the "key" order's details.
Expected payload syntax:

```
{ "productId": "ac334",
}
```
#### /product
Offers standard ModelViewSet operations.

Unprotected.

