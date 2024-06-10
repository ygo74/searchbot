
# Load private scripts
get-childitem -path "$PSScriptRoot\Private" -Recurse -File -Include "*.ps1"  | % {. $_.FullName}

# Load private scripts
get-childitem -path "$PSScriptRoot\Public" -Recurse -File -Include "*.ps1"  | % {. $_.FullName}