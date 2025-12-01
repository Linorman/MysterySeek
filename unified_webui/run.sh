#!/usr/bin/env bash
# Run script for MysterySeek Unified WebUI

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "🔍 MysterySeek Unified WebUI"
echo "=========================================="
echo ""

if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit is not installed. Please run:"
    echo "   pip install streamlit nest-asyncio"
    exit 1
fi

export PYTHONPATH="${SCRIPT_DIR}:${SCRIPT_DIR}/../AutoWerewolf:${SCRIPT_DIR}/../Echoes-of-Deceit-v2/src:$PYTHONPATH"

echo "🚀 Starting MysterySeek..."
echo ""

streamlit run app.py --server.headless true "$@"
