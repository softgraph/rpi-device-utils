# User Service (`systemd`)

- The following user service is used for `disp-mon`.
  - [disp_mon.service](<../disp_mon.service>)

- Run the command below to show the logging for the service.

```shell
$ journalctl --no-pager -b --user -u disp_mon
:
```
