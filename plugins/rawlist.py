from __future__ import unicode_literals, division, absolute_import
from builtins import *  # pylint: disable=unused-import, redefined-builtin

import logging
import re

from flexget import plugin
from flexget.event import event
from flexget.utils.cached_input import cached
from flexget.entry import Entry
from flexget.utils.soup import get_soup

log = logging.getLogger('rawlist')


class rawlist(object):
    """"Creates an entry for each movie or series in your MAL Plan to Watch and/or Watching lists."""

    @cached('rawlist', persist='2 hours')
    def on_task_input(self, task, config):

        def get_anime(task, url):
            log.verbose("Requesting %s" % url)
            page = task.requests.get(url, timeout=5)
            if page.status_code != 200:
                raise plugin.PluginError("Unable to get MAL list. Either the list is private or does not exist")
            soup = get_soup(page.text)

            anime_entries = page.text
            entries = []
            for anime_entry in anime_entries.splitlines():
                anime_entry = anime_entry.strip()
                entry = Entry()

                entry["title"] = anime_entry
                entry["myanimelist_name"] = anime_entry
                entry["url"] = "http://myanimelist.net" + anime_entry
                entries.append(entry)

            return entries

        # Create entries by parsing MAL wishlist page html using beautifulsoup
        url = 'https://pastebin.com/raw/XiFB0EF1'

        entries = []
        entries += get_anime(task, url)

        return entries


@event('plugin.register')
def register_plugin():
    plugin.register(rawlist, 'rawlist', api_ver=2, groups=['list'])
