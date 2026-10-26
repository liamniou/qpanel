import qbittorrentapi
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

def get_client(instance):
    """Creates and returns a qBittorrent client instance."""
    parsed_url = urlparse(instance.host)
    
    host = parsed_url.hostname
    port = parsed_url.port
    
    # Prepend scheme if it's missing, default to http
    scheme = parsed_url.scheme or 'http'
    full_host_url = f"{scheme}://{host}:{port}"

    try:
        client = qbittorrentapi.Client(
            host=full_host_url,
            username=instance.username,
            password=instance.password
        )
        return client
    except Exception as e:
        print(f"Failed to create qBittorrent client for {instance.name}: {e}")
        return None

def get_all_torrents(client, **kwargs):
    """
    Retrieves ALL torrents from qBittorrent in a single request.

    Don't paginate with limit/offset: qBittorrent resets an offset >= the torrent count to 0,
    so a count that's an exact multiple of the page size would loop forever on the first page.

    Returns an empty list if the request fails.
    """
    try:
        torrents = client.torrents_info(**kwargs)
        logger.info(f"Retrieved total of {len(torrents)} torrents")
        return torrents
    except Exception as e:
        logger.error(f"Error retrieving torrents: {e}")
        return []
