![](https://www.politico.com/interactives/cdn/images/badge.svg)

# template_lambda-etl

## Development docs

- [Deploying infrastructure](docs/deploying-infrastructure.md)

- [Developing bakery handlers](docs/developing-bakery-handlers.md)

- [Developing page assets](docs/developing-page-assets.md)


## Lambda environment

Once you deploy your Lambda instance, make sure you set these variables in its environment.

```
AWS_PUBLISH_ACCESS_KEY_ID=
AWS_PUBLISH_SECRET_ACCESS_KEY=
AWS_BUCKET_NAME=
AWS_CLOUDFRONT_DISTRIBUTION=
API_VERIFICATION_TOKEN=
```

The variable `LAMBDA` should already be set.

## Testing

To test, create a file named `dev/test/.env` using the `.env.example` in that folder as an example, and fill in the environment variables.


Now run:

```
$ yarn build
$ yarn test
```
