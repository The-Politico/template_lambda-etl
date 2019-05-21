![](https://www.politico.com/interactives/cdn/images/badge.svg)

# template_lambda-etl

## Development docs

- [Deploying infrastructure](docs/deploying-infrastructure.md)

- [Developing bakery handlers](docs/developing-bakery-handlers.md)

- [Developing page assets](docs/developing-page-assets.md)


## Lambda environment

Once you deploy your Lambda instance, make sure you set these variables in its environment.

```
API_VERIFICATION_TOKEN=
```

The variable `LAMBDA` should already be set.

## Testing

To test, create a file named `.env` using the `.env.example` in the project root as an example.


Now run:

```
$ pipenv install
$ pipenv run pytest
```
