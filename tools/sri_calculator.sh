#!/usr/bin/env bash

set -euo pipefail

INPUT="${1:-}"

if [[ -z "$INPUT" ]]; then
  echo "Usage: $0 <file-or-url>"
  exit 1
fi

# Function to compute SHA-384 base64 hash
hash_stream() {
    printf "sha384-%s\n" "$(openssl dgst -sha384 -binary | openssl base64 -A)"
}

# Check if input is a URL
if [[ "$INPUT" =~ ^https?:// ]]; then
  # URL case
  curl -fsSL "$INPUT" | hash_stream

elif [[ -f "$INPUT" ]]; then
  # File case
  cat "$INPUT" | hash_stream

else
  echo "Error: input is neither a valid file nor a supported URL"
  exit 1
fi
