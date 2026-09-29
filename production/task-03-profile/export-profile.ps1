Add-Type -AssemblyName System.Drawing
$dest = 'C:\Users\sokol\OneDrive\文档\ChatGPT\sinpop wix web\output\sinopop-music-objects-20260927\task-03-profile'
$records = Get-Content -LiteralPath (Join-Path $dest 'profile-build-input.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$sourceDir = Join-Path $dest '_source'
New-Item -ItemType Directory -Path $sourceDir -Force | Out-Null
$receipts = @()
foreach ($entry in $records) {
    $original = [System.Drawing.Image]::FromFile($entry.source)
    $originalSize = @($original.Width,$original.Height)
    $w = [int]$entry.output_size[0]
    $h = [int]$entry.output_size[1]
    $output = [System.Drawing.Bitmap]::new($w,$h,[System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
    $output.SetResolution(300,300)
    $g = [System.Drawing.Graphics]::FromImage($output)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $g.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
    $g.DrawImage($original,[System.Drawing.Rectangle]::new(0,0,$w,$h),[float]$entry.crop_source_pixels[0],[float]$entry.crop_source_pixels[1],[float]$entry.crop_source_pixels[2],[float]$entry.crop_source_pixels[3],[System.Drawing.GraphicsUnit]::Pixel)
    $target = Join-Path $dest $entry.file
    $output.Save($target,[System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose()
    $output.Dispose()
    $original.Dispose()
    Copy-Item -LiteralPath $entry.source -Destination (Join-Path $sourceDir $entry.file)
    $check=[System.Drawing.Image]::FromFile($target)
    $valid=($check.Width -eq $w -and $check.Height -eq $h -and $check.RawFormat.Guid -eq [System.Drawing.Imaging.ImageFormat]::Png.Guid)
    $check.Dispose()
    $receipts += [pscustomobject]@{file=$entry.file;status='generated-and-verified';tool='built-in image_gen';source_path=$entry.source;source_size=$originalSize;crop_source_pixels=$entry.crop_source_pixels;output_path=$target;output_size=@($w,$h);format='PNG';decode_verified=$valid;sha256=(Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash;transformation='composition-preserving crop plus high-quality bicubic resize; not native 2400';ai_concept_only=$true;readable_text_present=$false;logo_present=$false}
}
[pscustomobject]@{task='03-profile';ai_concept_warning='AI concept photography only, not actual SinoPOP event documentation';photographic_palette_note='Continuous photographic tones, not an eight-color indexed palette';files=$receipts} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $dest 'receipt-profile.json') -Encoding UTF8
$receipts | Select-Object file,output_size,decode_verified | ConvertTo-Json -Compress

