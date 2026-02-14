#!/bin/bash
# Build script for Render deployment
# Installs CPU-only PyTorch to avoid CUDA dependencies and hash mismatches

set -e

echo "Installing CPU-only PyTorch..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

echo "Installing remaining requirements..."
pip install -r requirements.txt

echo "Build complete!"

