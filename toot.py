#!/usr/bin/env python3

from mastodon import Mastodon
import sys
import argparse
import os
import secureconfig

BASE_URL = 'https://anticapitalist.party'
CONFIG_ROOT = os.path.expanduser('~/.config/fedi')
USER_SECRET = CONFIG_ROOT + '/fd-user.secret'
CLIENT_SECRET = CONFIG_ROOT + '/fd-client.secret'

def get_mastodon():
	return Mastodon(
			access_token = USER_SECRET,
			api_base_url = BASE_URL,
		)

def register():
	os.mkdir(CONFIG_ROOT)
	Mastodon.create_app(
			'fd',
			api_base_url = BASE_URL,
			to_file = CLIENT_SECRET,
		)
	mastodon = Mastodon(
			client_id = CLIENT_SECRET,
			api_base_url = BASE_URL,
		)
	mastodon.log_in(
			secureconfig.USERNAME,
			secureconfig.PASSWORD,
			to_file = USER_SECRET,
		)
	return mastodon

if __name__ == '__main__':
	mastodon = None
	if os.path.isfile(USER_SECRET):
		mastodon = get_mastodon()
	else:
		mastodon = register()

	toot = sys.stdin.read()

	if toot:
		mastodon.toot(toot)

