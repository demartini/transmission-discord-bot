<!-- LOGO -->
<div align="center">
  <img align="center" src=".github/media/bot-logo.png?raw=true" alt="Bot Logo" width="200">
</div>

<h1 align="center">Transmission Discord Bot</h1>

<!-- SHIELDS -->
<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

</div>

<!-- TABLE OF CONTENTS -->

## Table of Contents <!-- omit in toc -->

- [About](#about)
- [Features](#features)
  - [Commands](#commands)
- [Usage](#usage)
  - [Docker Compose (Recommended)](#docker-compose-recommended)
  - [Docker CLI](#docker-cli)
  - [Source](#source)
- [Parameters](#parameters)
- [Environment variables from files (Docker secrets)](#environment-variables-from-files-docker-secrets)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [License](#license)

<!-- ABOUT -->

## About

The Transmission Discord Bot is a Python-based Discord bot built with the [interactions.py][interactions-url] framework. It seamlessly integrates with your Transmission BitTorrent client, empowering you to manage your downloads directly through Discord using intuitive slash commands. This user-friendly bot simplifies your torrent management experience, allowing you to effortlessly `add`, `remove`, `list`, `pause`, and `resume` torrents without ever leaving your favorite Discord server.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- FEATURES -->

## Features

- **Torrent Management Made Easy:** Interact with your Transmission BitTorrent client directly from Discord.
- **Intuitive Slash Commands:** Execute commands with the simple and familiar `/torrents` syntax.
- **Comprehensive Actions:**
  - **Add:**  Add torrents by URL or magnet link, optionally specifying download directory.
  - **List:**  View a list of active torrents with progress information.
  - **Pause:** Pause active torrents.
  - **Resume:** Resume paused torrents.
  - **Remove:** Remove torrents and optionally delete downloaded data.
- **Informative Embeds:** All bot responses are presented in visually appealing embeds for clarity and organization.
- **Error Handling:** Robust error handling ensures a smooth user experience and provides helpful feedback in case of issues.
- **Logging:** Detailed logging helps with troubleshooting and bot maintenance.
- **Help Command:**  A dedicated `/torrents help` command provides clear instructions on how to use all bot functionalities.

**For full documentation and examples, please refer to the [Documentation][documentation-url].**

<!-- COMMANDS -->

### Commands

| **Command**                                        | **Description**   |
| -------------------------------------------------- | ----------------- |
| `/torrents add <url> [destination:<download_dir>]` | Add a torrent.    |
| `/torrents list`                                   | List torrents.    |
| `/torrents pause <id>`                             | Pause a torrent.  |
| `/torrents remove <id>`                            | Remove a torrent. |
| `/torrents resume <id>`                            | Resume a torrent. |
| `/torrents help`                                   | Get help.         |

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE -->

## Usage

To help you get started creating a container from this image you can either use docker-compose or the docker cli.

<!-- DOCKER-COMPOSE -->

### Docker Compose (Recommended)

```yaml
---
services:
  transmission-discord-bot:
    container_name: transmission-discord-bot
    image: demartini/transmission-discord-bot:latest
    restart: unless-stopped
    environment:
      DISCORD_TOKEN: XXXXXXXXXX
      SERVER_ID: XXXXXXXXXX
      TRANSMISSION_HOST: localhost
      TRANSMISSION_PORT: 9091
      TRANSMISSION_USERNAME: admin
      TRANSMISSION_PASSWORD: password
    volumes:
      - ./logs:/app/logs
```

<!-- DOCKER CLI -->

### Docker CLI

```bash
docker run -d \
  --name=transmission-discord-bot \
  -e DISCORD_TOKEN= \
  -e SERVER_ID= \
  -e TRANSMISSION_HOST= \
  -e TRANSMISSION_PORT= \
  -e TRANSMISSION_USERNAME= \
  -e TRANSMISSION_PASSWORD= \
  -v /path/to/logs:/app/logs \
  --restart unless-stopped \
  demartini/transmission-discord-bot:latest
```
<!-- SOURCE -->

### Source

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/demartini/transmission-discord-bot
   ```

2. **Install Dependencies:**

   - **Option 1: Using Poetry (Recommended):**

      ```bash
      cd transmission-discord-bot
      poetry install
      ```

   - **Option 2: Without Poetry:**

      ```bash
      cd transmission-discord-bot
      python -m venv venv  # Create a virtual environment (optional but recommended)
      source venv/bin/activate  # Activate virtual env (Linux/macOS) or venv\Scripts\activate (Windows)
      pip install -r requirements.txt
      ```

3. **Create a `.env` File:**

   - Copy the provided `.env.example` file and rename it to `.env`.
   - Fill in the required values in the `.env` file, including your Discord bot token and Transmission server details.

4. **Start the Bot:**

   - **If using Poetry:**

      ```bash
      poetry shell  # Optional: Activate the virtual environment (if not already active)
      poetry run python src/main.py
      ```

   - **Without Poetry:**

      ```bash
      python src/main.py
      ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- PARAMETERS -->

## Parameters

Containers are configured using parameters passed at runtime (such as those above).

|         Parameter          | Function                                                                   |
| :------------------------: | -------------------------------------------------------------------------- |
|     `-e DISCORD_TOKEN`     | Your Discord bot's token from the Developer Portal.                        |
|       `-e SERVER_ID`       | The Discord server ID where the bot should operate.                        |
|   `-e TRANSMISSION_HOST`   | The hostname or IP address of your Transmission server. (e.g., localhost). |
|   `-e TRANSMISSION_PORT`   | The port used by Transmission's RPC interface. (e.g., 9091).               |
| `-e TRANSMISSION_USERNAME` | Your Transmission username if required.                                    |
| `-e TRANSMISSION_PASSWORD` | Your Transmission password if required.                                    |
|       `-v /app/logs`       | Logs directory in the container.                                           |

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ENVIRONMENT -->

## Environment variables from files (Docker secrets)

You can set any environment variable from a file by using a special prepend `FILE__`.

As an example:

```bash
-e FILE__MYVAR=/run/secrets/mysecretvariable
```

Will set the environment variable `MYVAR` based on the contents of the `/run/secrets/mysecretvariable` file.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

If you are interested in helping contribute, please take a look at our [contribution guidelines][contributing-url] and open an [issue][issues-url] or [pull request][pull-request-url].

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CHANGELOG -->

## Changelog

See [CHANGELOG][changelog-url] for a human-readable history of changes.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See [LICENSE][license-url] for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->

[changelog-url]: https://github.com/demartini/transmission-discord-bot/blob/main/CHANGELOG.md
[contributing-url]: https://github.com/demartini/.github/blob/main/CONTRIBUTING.md
[pull-request-url]: https://github.com/demartini/transmission-discord-bot/pulls

[contributors-shield]: https://img.shields.io/github/contributors/demartini/transmission-discord-bot.svg?style=for-the-badge&color=8bd5ca&labelColor=181926
[contributors-url]: https://github.com/demartini/transmission-discord-bot/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/demartini/transmission-discord-bot.svg?style=for-the-badge&color=8bd5ca&labelColor=181926
[forks-url]: https://github.com/demartini/transmission-discord-bot/network/members
[issues-shield]: https://img.shields.io/github/issues/demartini/transmission-discord-bot.svg?style=for-the-badge&color=8bd5ca&labelColor=181926
[issues-url]: https://github.com/demartini/transmission-discord-bot/issues
[license-shield]: https://img.shields.io/github/license/demartini/transmission-discord-bot.svg?style=for-the-badge&color=8bd5ca&labelColor=181926
[license-url]: https://github.com/demartini/transmission-discord-bot/blob/main/LICENSE
[stars-shield]: https://img.shields.io/github/stars/demartini/transmission-discord-bot.svg?style=for-the-badge&color=8bd5ca&labelColor=181926
[stars-url]: https://github.com/demartini/transmission-discord-bot/stargazers

[documentation-url]: https://docs.demartini.dev/projects/transmission-discord-bot
[interactions-url]: https://github.com/interactions-py/interactions.py
