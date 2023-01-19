
# Creating OpenID Connect Authentication Provider

Here you will find all the steps for creating your own OpenID Connect authentication provider (more details below).

## Summary 

- [Summary](#summary)
- [API's routes](#apis-routes)
- [Database](#database)

## API's routes

### Validate Client ID and Access Token provided by frontend

```http
  POST /sso/auth
```

| Query Params   | Type       | Description                           |
| :---------- | :--------- | :---------------------------------- |
| `client_id` | `string` |A key registered in client table in database|
| `redirect_uri` | `string` |Uri to send the route with the params "state" and "code"|
| `response_type` | `string` |Value must be "code" |
| `scope` | `string` |Space separated scopes to request for the token. Must contain at least *'openid'*|
| `state` | `string` | String used to generate the response code |
| `access_key` | `Form` | User's access key to API |

#### This route validates client_id and redirect_uri in database, generating a session_code based on state.
#### Next, it updates users table, inserting the generated code in the column *session_code* (API gets the user id through decoding access_key). The code is returned with state as parameters to redirect_uri.
    
    request example: https://example/sso/auth?client_id=client_example&response_type=code&redirect_uri=https://redirect_uri_example.com/&scope=openid&state=state_example

    response example: RedirectResponse(url=f'{redirect_uri}?state={state}&code={code}')

### Generate access token to applicant app

```http
  POST /sso/token
```  

| Body Parameters   | Type | Description                           |
| :---------- | :--------- | :---------------------------------- |
| `client_id` | `string` | A key registered in client table in database |
| `client_secret` | `string (Optional)` | Secret registered with client_id in client table |
| `redirect_uri` | `string` | URI registered with client_id in client table |
| `code` | `string` | Session code created through previous route *'/sso/auth'* |

#### This route validates request body and search for an user with the session_code value equal to the code sent in the request. After that, two JWT's are generated, one with the username value inside id_token key and another with the user id inside access_token key.

       example:
            id_token = create_access_token(data={'sub': user.username})
            access_token = create_access_token(data={'sub': str(user.id)})

            return {
                'access_token': access_token,
                'token_type': 'Bearer',
                'expires_in': 1800,
                'id_token': id_token
            }

### Send more user info

```http
  GET /sso/user_info
```  

#### This route searchs in users table for details of the user to send to applicant app based on user id inside the decoded access_token sent in the headers of request.

        example: 
             return {
              'sub': user.username,
              'name': user.name,
              'email': user.email
            }

## Database
#### Inside `alembic > versions` can be found the models for the needed tables in order to run the provider.
