# LTD2-DSS

## Environment Variables

```console
$ cp env.template .env
```

Fill env variable with your API key from https://developer.legiontd2.com/home - key_management
```
LTD2_X_API_KEY=xxx
```

When faced:
```
Xlib.error.DisplayConnectionError: Can't connect to display ":0": b'Authorization required, but no authorization protocol specified\n'
```
To enable display access use:
```
$ xhost +
```
