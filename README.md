Address Service
====

# Quick Start

```shell
docker compose up --build
```

Registration:

http://localhost:8000/accounts/signup

Login:

http://localhost:8000/accounts/login

Log out:

http://localhost:8000/accounts/logout

Social auth is currently unsupported.

Create and list addresses:

http://localhost:8000/addresses/

Get Update Delete addresses:

http://localhost:8000/addresses/{id}

# About

A simple REST API for managing users addresses.

The scope is limited to residential addresses.

The service attempts to take into account that not all countries require a postal code, though some countries do.  If a country is know to require a postal code the API enforces the postal_code as required.  In all other cases the postal code is optional.

Postal codes are validated but checking they can be found within the provided country.

Country codes are validated against an ISO list of country codes.

First name and Last name can be different than the user account first name and last name.

The service allows for localization of country names based on [Django's language preference discovery](https://docs.djangoproject.com/en/4.0/topics/i18n/translation/#how-django-discovers-language-preference), and defaults to en-us.

The user must be authenticated to fetch or change thier address information.

# Further Development

The security of the data in this application is light, and is not sufficent to protect data this sensative.  In later iterations, encrypting data in transit and at rest would be enforced, data access would be logged.  An admin interface would be introduced and data not required for an admin user to perform thier jobs would be restricted and redacted.

Validate city is within the given country and normalize it's value.  Validate postal code, city and country are consistent with eachother.

Accounts should be managed by a seperate system.  If accounts continue to be managed here, a rest API should be favored over an HTML page.

Add test coverage.
