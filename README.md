# qPanel

qPanel is a web-based management tool for qBittorrent, designed to automate torrent management tasks such as:

- applying seeding rules (i.e. `if a torrent has tag noHL, set seeding time to 43200 minutes`);
- finding torrents without hard links;
- pausing cross-seeded torrents;
- finding unregistered torrents.

![demo](qpanel_demo.gif "qPanel demo")

The tool can:
- apply rules to torrents that match the specified criteria, for example:
    - If a torrent has tag `noHL`, set `Share Limit Time` to `43200 minutes`;
    - If one of the `trackers` is `bt.t-ru.org`, set `Max Upload Speed (KiB/s)` to `10`.
- tag torrents that don't have hard links with tag `noHL` (useful for torrent clients used by Sonarr/Radarr), optionally skipping completed downloads that are still waiting for import in Sonarr/Radarr (e.g. "Manual Import required");
- pause cross-seeded torrents;
- tag "unregistered" torrents with tag `unregistered`;
- remove the qBittorrent category from completed downloads that Sonarr/Radarr won't import because they are "Not a Custom Format upgrade" for existing files, so they leave the arr queue but keep seeding (configure Sonarr/Radarr instances under **Instances**).

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/liamniou/qpanel.git
    cd qpanel
    ```

2.  **Create a `.env` file** to specify the port you want to run the application on:
    ```
    FLASK_PORT=5000
    ```

3.  **Run the application:**
    ```bash
    docker compose up -d
    ```

4.  **Access the application** by navigating to `http://localhost:5000` in your web browser.

## Configuration

All configuration is done through the web interface:

- **Instances** – your qBittorrent clients and the Sonarr/Radarr instances qPanel talks to. Each qBittorrent instance has its own page with sections for *Connection*, *Download paths*, *Hard links (noHL)*, *Torrent hygiene* (cross-seed pausing, unregistered tagging), *Orphaned files* and *Rules* (assign rules to the instance).
- **Rules** – reusable seeding/speed limits, matched by tracker, tag or category (exact category name). Each instance runs its assigned rules top to bottom in its own order (reorder them with the arrows in the instance's *Rules* section): every matching rule applies, a later rule overrides limits set by an earlier one, and a rule with **Stop processing other rules** ends the chain for torrents it matches (leave its limits empty for a pure "stop" rule).
- **Activity** – the action log and orphaned files found by the scanner.
- **Settings** – scheduler interval, cache, notifications (Telegram/Discord) and maintenance actions. 
