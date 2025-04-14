#!/bin/bash

ENV_FILE=".env"
CREDENTIALS_FILE="credentials.json"

echo "🔧 Setting up your .env file for contentgen..."

read -p "👉 OpenAI API Key: " OPENAI_API_KEY
read -p "👉 Google Sheet ID: " SHEET_ID
read -p "👉 Company Name (e.g. Harness): " COMPANY_NAME
read -p "👉 Company Site URL (e.g. developer.harness.io): " SITE_URL

echo "📋 Paste your Google service account credentials JSON below."
echo "💡 When done, press CTRL+D (Linux/macOS) or CTRL+Z (Windows) to save."
cat > "$CREDENTIALS_FILE"

if [ ! -s "$CREDENTIALS_FILE" ]; then
  echo "❌ No content saved to $CREDENTIALS_FILE. Aborting."
  exit 1
fi

cat <<EOF > "$ENV_FILE"
# === Required Keys ===

OPENAI_API_KEY=$OPENAI_API_KEY
SHEET_ID=$SHEET_ID
GOOGLE_CREDENTIALS_PATH=./$CREDENTIALS_FILE

# === Customization (Optional) ===

COMPANY_NAME=$COMPANY_NAME
SITE_URL=$SITE_URL
EOF

echo "✅ .env created successfully!"
echo "📁 Saved credentials to $CREDENTIALS_FILE"
echo "💡 Tip: You can now run contentgen via Docker or CLI."

# Optional: Copy to Docker-friendly path
read -p "🐳 Copy .env to ~/.contentgen.env for Docker use? (y/N): " COPY_ENV
if [[ "$COPY_ENV" =~ ^[Yy]$ ]]; then
  cp "$ENV_FILE" ~/.contentgen.env
  echo "✅ Copied to ~/.contentgen.env"
fi