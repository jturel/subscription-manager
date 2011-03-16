#
# Copyright (c) 2010 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
#
# Red Hat trademarks are not licensed under GPLv2. No permission is
# granted to use or replicate Red Hat trademarks that are incorporated
# in this software or its documentation.
#

"""
Helper methods for mocking up JSON model objects, certificates, etc.
"""

#import hashlib

import md5

from datetime import timedelta, datetime
from mock import Mock
from random import randint

def create_pool(product_id, product_name, quantity=10, consumed=0, provided_products=[]):
    """
    Returns a hash representing a pool. Used to simulate the JSON returned
    from Candlepin.
    """
    provided = []
    for pid in provided_products:
        provided.append({
            'productId': pid,
            'productName': pid,
        })

    md5sum = md5.new()
    md5sum.update(product_id)
    id = md5sum.hexdigest()
#    id = hashlib.md5(product_id).hexdigest()

    return {
            'productName': product_name,
            'productId': product_id,
            'quantity': quantity,
            'consumed': consumed,
            'id': id,
            'subscriptionId': '402881062bc9a379012bc9a3d7380050',
            'startDate': datetime.now() - timedelta(days=365),
            'endDate': datetime.now() + timedelta(days=365),
            'updated': datetime.now() - timedelta(days=365),
            'created': datetime.now() - timedelta(days=365),
            'activeSubscription': True,
            'providedProducts': provided,
            'sourceEntitlement': None,
            'href': '/pools/%s' % id,
            'restrictedToUsername': None,
            'owner': {
                'href': '/owners/admin',
                'id': '402881062bc9a379012bc9a393fe0005'},
            'attributes': [],
        }

