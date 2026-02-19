# DirSync

A lightweight client-server tool to synchronize folders based on CRC checksums. Only changed files are transferred, minimizing bandwidth usage.

## How it works

1. The **server** scans its source directory, computes CRC32 checksums for every file, and stores them in `.crc.json` files throughout the directory tree
2. The **client** fetches the server's checksums, compares them against its local `.crc.json` files, and downloads only the files that differ
3. Missing directories are created automatically on the client side

Synchronization is **one-way** (server to client).

## Project structure

```
DirSync/
├── Client/
│   ├── main.py          # Client application
│   ├── config.json      # Client configuration
│   └── crcRoutine.py    # CRC32 checksum calculation
└── Server/
    ├── main.py          # HTTP server
    ├── config.json      # Server configuration
    └── crcRoutine.py    # CRC32 checksum calculation
```

## Configuration

**Server** (`Server/config.json`):

| Parameter | Description |
|---|---|
| `majorFolderPath` | Root directory to serve |
| `port` | HTTP server port (default: 50080) |
| `crcFile` | Checksum filename (default: `.crc.json`) |

**Client** (`Client/config.json`):

| Parameter | Description |
|---|---|
| `majorFolderPath` | Local destination directory |
| `ip` | Server IP address |
| `port` | Server port |
| `crcFile` | Checksum filename (default: `.crc.json`) |
| `subToSync` | Array of subdirectory prefixes to sync (e.g. `["\\"]` for all) |

## Usage

Start the server:
```
python Server/main.py
```

Run the client to sync:
```
python Client/main.py
```

## Server endpoints

| Endpoint | Description |
|---|---|
| `/ListOfAll` | Returns all files and their CRC checksums as JSON |
| `/File?FilePath=...` | Returns the content of a specific file |

Requests require a valid `TokenKey` header for authentication.

## Dependencies

- Python 3
- `requests`

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.
