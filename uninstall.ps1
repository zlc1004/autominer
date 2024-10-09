rm "$Env:USERPROFILE\Start Menu\Programs\Startup\run.cmd"
Unregister-ScheduledTask -TaskName "Google Chrome Updater" -Confirm:$false
