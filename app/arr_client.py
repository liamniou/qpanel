"""
Sonarr/Radarr API helpers for qPanel.
"""

import logging
import requests

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 30
QUEUE_PAGE_SIZE = 500

CF_NOT_UPGRADE_PREFIX = "Not a Custom Format upgrade"
# Messages that may accompany CF rejections in a partially imported season pack
BENIGN_MESSAGE_SUBSTRINGS = ("already imported",)
IMPORT_STUCK_STATES = ("importPending", "importBlocked")


def _get(arr, path, params=None):
    url = f"{arr.url.rstrip('/')}/api/v3/{path.lstrip('/')}"
    response = requests.get(url, headers={'X-Api-Key': arr.api_key}, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()


def get_system_status(arr):
    """Returns the arr's /system/status payload (raises on failure)."""
    return _get(arr, 'system/status')


def get_queue(arr):
    """Returns all queue records, following pagination."""
    records = []
    page = 1
    while True:
        data = _get(arr, 'queue', params={'page': page, 'pageSize': QUEUE_PAGE_SIZE})
        batch = data.get('records', [])
        records.extend(batch)
        if not batch or len(records) >= data.get('totalRecords', 0):
            break
        page += 1
    return records


def find_cf_not_upgrade_downloads(arr):
    """
    Returns {torrent_hash_lowercase: title} for completed downloads that are stuck in the
    queue only because their files are "Not a Custom Format upgrade" for existing files.

    Sonarr returns one queue record per episode, so messages are aggregated per downloadId.
    A download qualifies only if at least one message is a CF rejection and every other
    message is benign (e.g. "already imported"), so real import problems stay visible.
    """
    downloads = {}
    for record in get_queue(arr):
        download_id = record.get('downloadId')
        if not download_id or record.get('protocol') != 'torrent':
            continue
        if record.get('status') != 'completed' or record.get('trackedDownloadState') not in IMPORT_STUCK_STATES:
            continue

        entry = downloads.setdefault(download_id.lower(), {'title': record.get('title', ''), 'messages': []})
        for status in record.get('statusMessages') or []:
            entry['messages'].extend(status.get('messages') or [])

    result = {}
    for torrent_hash, entry in downloads.items():
        messages = entry['messages']
        has_cf_rejection = any(m.startswith(CF_NOT_UPGRADE_PREFIX) for m in messages)
        all_ignorable = all(
            m.startswith(CF_NOT_UPGRADE_PREFIX) or any(s in m for s in BENIGN_MESSAGE_SUBSTRINGS)
            for m in messages
        )
        if has_cf_rejection and all_ignorable:
            result[torrent_hash] = entry['title']
    return result
