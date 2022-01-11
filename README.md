# adamsnimbus.info

AWS CDK to deploy a simple static website.

Entrypoints all run inside a container built for purpose - [aws-cdk-v2](ghcr.io/adamsnimbus/aws-cdk-v2:2.3.0)

# Instructions

Makefile is used to expose most common required AWS CDK commands, for example:
```bash
- make diff
- make synth
- make deploy
```

All variables are consumed via [cdk.json](cdk.json) & required Env vars via [docker-compose.yml](docker-compose.yml)

# Troubleshooting
Use `make shell` to shell into the container and fool around...
