# Luma API MCP

A Model Context Protocol (MCP) server that provides AI image and video generation capabilities using the Luma API.

## Setup

### Automatic Setup (Recommended)

1. Install Claude Desktop App or any MCP client
2. Get API Key from https://lumalabs.ai/api/keys
3. Run `sh setup.sh`, here it will ask the API Key - paste it from step 2
4. The script will automatically configure Claude Desktop and restart it

### Manual Setup

1. Install dependencies:

   ```bash
   pip install mcp[cli] aiohttp
   ```

2. Set your Luma API key:

   ```bash
   export LUMA_API_KEY='your-api-key-here'
   ```

3. Run the server locally:

   ```bash
   python main.py
   ```

   Or using uv:

   ```bash
   uv run --python python3.10 --with mcp[cli] --with aiohttp mcp run server.py
   ```

### Manual Host Configuration (e.g. VS Code, Windsurf, Cursor, etc.)

Add this to your JSON config file:

```json
{
  "luma-api-mcp": {
    "command": "uv",
    "args": [
      "--directory",
      "/Users/user123/luma-api-mcp",
      "run",
      "main.py"
    ],
    "disabled": false,
    "alwaysAllow": [],
    "env": {
      "LUMA_API_KEY": "your-api-key-here"
    }
  }
}
```

## Features

### Create Image

- `prompt`: text
- `aspect_ratio`: "1:1", "16:9", "9:16", "4:3", "3:4", "21:9", "9:21" (default: "16:9")
- `model`: "photon-1", "photon-flash-1" (default: "photon-1")
- `image_ref`: list of image URLs with weights to influence generation (optional), max 8
- `style_ref`: single image URL with weight to influence style (optional), max 1
- `character_ref`: list of character image URLs (optional), max 4
- `modify_image_ref`: single image URL to modify with weight (optional), max 1

### Create Video

- `prompt`: text
- `aspect_ratio`: "1:1", "16:9", "9:16", "4:3", "3:4", "21:9", "9:21" (default: "16:9")
- `model`: "ray-2", "ray-flash-2", "ray-1-6" (default: "ray-2")
- `loop`: boolean (default: false)
- `resolution`: "540p", "720p", "1080p", "4k" (default: "720p")
- `duration`: "5s", "9s" (default: "5s")
- `frame0_image`: image URL (optional)
- `frame1_image`: image URL (optional)
- `frame0_id`: generation ID (optional)
- `frame1_id`: generation ID (optional)

## Technical Notes

- Keyframes: Providing frame0_image/frame1_image gives more control over video start/end points
- Video Response Time: Typical video generation takes 15-60 seconds depending on duration and resolution
- Image Response Time: Typical generation takes 5-15 seconds depending on model complexity
