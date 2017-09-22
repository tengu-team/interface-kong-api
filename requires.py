#!/usr/bin/env python3
# Copyright (C) 2017  Qrama, developed by Tengu-team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# pylint: disable=c0111,c0301,c0325, r0903,w0406
from charms.reactive import hook, RelationBase, scopes


class KongAPIRequires(RelationBase):
    scope = scopes.UNIT

    @hook('{requires:kong-api}-relation-joined')
    def joined(self):
        for conv in self.conversations():
            conv.set_state('{relation_name}.connected')

    @hook('{requires:kong-api}-relation-changed')
    def changed(self):
        for conv in self.conversations():
            if conv.get_local('upstream_url'):
                conv.set_state('{relation_name}.available')

    @hook('{requires:kong-api}-relation-departed')
    def departed(self):
        for conv in self.conversations():
            conv.remove_state('{relation_name}.connected')

    @hook('{requires:kong-api}-relation-broken')
    def broken(self):
        for conv in self.conversations():
            conv.remove_state('{relation_name}.available')

    def add_api(self, service, upstream_url, hosts=[], uris=[], methods=[]):
        for conv in self.conversations():
            api_info = {
                'service': service,
                'upstream_url': upstream_url,
                'hosts': ','.join(hosts),
                'uris': ','.join(uris),
                'methods': ','.join(methods),
                }
            conv.set_local(**api_info)
            conv.set_remote(**api_info)
