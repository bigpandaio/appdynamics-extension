# BigPanda Appdynamics Extension
An Appdynamics custom action that sends alerts to BigPanda

## Installation

1. Download the zip release and unpack it to `<CONTROLLER INSTALL ROOT>/custom/actions`

2. Update or create `<CONTROLLER INSTALL ROOT>/custom/actions/custom.xml`. The file should look like this:

```xml
<custom-actions>
  <action>
    <type>bigpanda-alert</type>
    <executable>bigpanda_alert.py</executable>
  </action>
  ...your other actions...
</custom-actions>
```

## Configuration

Edit `<CONTROLLER INSTALL ROOT>/custom/actions/bigpanda-alert/config.ini` and set your API token and app key:

```ini
[base]
api_token: <YOUR API TOKEN>
app_key: <YOUR APP_KEY>
logging: no
```

You can enable logging for debug purposes. The log will be at `/tmp/bigpanda-alert.log`

## Releasing

Create a release branch (git-flow) with the new version, bump the version inside bigpanda-alert/bigpanda-alert.py, commit and merge it back into develop and master. Logic changes should bump minor version (e.g. 1.3 to 1.4) while minor fixes should bump patch version (e.g. 1.3 to 1.3.1).

## Deploying

The script is packages and deployed automatically by Travis CI once all tests pass successfully on the tagged commit. Artifacts are uploaded to S3 to the bp-appdynamic-extension bucket.
