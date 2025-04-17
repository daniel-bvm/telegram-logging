# telegram-logging

Module to notify unhandled error for beta running app

## Installtion

This module requires `python 3.9+` (with `pip` installed) to run. To install, just simply execute:

```bash
python -m pip install git+$<link-to-this-repo>
```

## Setup

The module requires two environment variables:

```bash
TELEGRAM_ROOM=<value>
TELEGRAM_BOT_TOKEN=<value> 
```

## Usage

```python
# normal usage
from telelog import log
log('a message, stacktrace or whatever')

# or in a asynchronous context
from telelog import alog 
await alog('a message, stacktrace or whatever')
```

