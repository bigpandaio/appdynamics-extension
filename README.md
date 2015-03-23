# BigPanda Appdynamics Extension
An Appdynamics custom action that sends alerts to BigPanda

## Installation

1. Download the zip release and unpack it to `<CONTROLLER INSTALL ROOT>/custom/actions`

2. Update or create `<CONTROLLER INSTALL ROOT>/custom/actions/custom.xml`. The file should look like this:

```
<custom-actions>
  <action>
    <type>bigpanda</type>
    <executable>bigpanda-alert.py</executable>
  </action>
  ...your other actions...
</custom-actions>
```

3. Edit `<CONTROLLER INSTALL ROOT>/custom/actions/bigpanda-alert/config.ini` and set your API token and app key:

```ini
[base]
api_token: <YOUR API TOKEN>
app_key: <YOUR APP_KEY>
logging: no
```
