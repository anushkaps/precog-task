# How to Run Your Notebook on Modal GPU

## Quick Start

### Option 1: Simple Test (Recommended First)

1. **Make sure Modal is installed and authenticated:**
   ```bash
   pip install modal
   python -m modal setup
   ```

2. **Upload your notebook to Modal:**
   The easiest way is to use git or upload files. For now, let's use a simpler approach.

### Option 2: Using Git (Best for Full Project)

If your code is in a git repo:

1. **Update the Modal script to clone your repo:**
   ```python
   # In the function, add:
   subprocess.run(["git", "clone", "YOUR_REPO_URL", "/root/project"])
   ```

2. **Run:**
   ```bash
   modal run run_modal_simple.py
   ```

### Option 3: Manual File Upload

1. **Create a zip of your project:**
   ```bash
   # On Windows PowerShell:
   Compress-Archive -Path . -DestinationPath project.zip
   ```

2. **Upload to Modal and extract in the function**

## Recommended: Use Modal's Web Interface

The easiest way is to:

1. **Go to Modal dashboard:** https://modal.com/apps
2. **Create a new app**
3. **Upload your notebook file**
4. **Run it with GPU enabled**

## Or Use This Simple Script

I've created `run_modal_simple.py` as a template. You need to:

1. **Add your notebook code** to the function
2. **Or upload your files** to Modal's file system
3. **Run:** `modal run run_modal_simple.py`

## Download Outputs

After running:
```bash
modal volume download lazy-artist-outputs ./outputs
```

## Need Help?

The Modal API for file mounting has changed. The best approach now is:
- Use git to clone your repo in the function
- Or upload files via Modal's web interface
- Or use Modal's file upload API

Would you like me to create a version that uses git, or would you prefer to upload files manually?

