import argparse
import ConfigParser
import random
import string

from decimal import Decimal
from Tenant import Tenant
from formatter import NegativeParenFormatter

parser = argparse.ArgumentParser()

cfg = ConfigParser.RawConfigParser()
cfg.read('config.ini')

total_rent = Decimal(cfg.get('MAIN', 'total_rent'))
last_plus = cfg.get('MAIN', 'last_plus')
last_minus = cfg.get('MAIN', 'last_minus')

fmoney = "${:,.2f}"

f = NegativeParenFormatter()

tenants = []

for tenant in [section for section in cfg.sections() if section != 'MAIN']:
    name = tenant.title()
    rent = cfg.get(tenant, 'rent')
    utilities = cfg.get(tenant, 'utilities').split(',') if cfg.has_option(tenant, 'utilities') else []
    tenants.append(Tenant(name, rent, utilities))

for u in [utility for tenant in tenants for utility in tenant.utilities.keys()]:
    parser.add_argument('-' + u, '-' + u[0], nargs=1, type=Decimal, required=True, dest=u)

args = vars(parser.parse_args())

total_utilities = sum(arg[0] for arg in args.values())
tenant_owes = (total_utilities / len(tenants)).quantize(Decimal('.01'))

for tenant in tenants:
    tenant.owes = tenant_owes
    for utility in tenant.utilities.keys():
        for arg in args.keys():
            if arg == utility:
                tenant.utilities[utility] = args[arg][0]

difference = sum([tenant.total() for tenant in tenants]) - total_rent

if difference == 0:
    pass
elif difference > 0:
    new_plus = random.choice([tenant for tenant in tenants if tenant.name.lower() != last_plus.lower()])
    new_plus.adjustment = difference
elif difference < 0:
    new_minus = random.choice([tenant for tenant in tenants if tenant.name.lower() != last_minus.lower()])
    new_minus.adjustment = difference

print "Breakdown:"

print ""

print "Each of us paid this much in utilities:"

for tenant in tenants:
    tenant_utils = [u for k, u in tenant.utilities.iteritems()]
    line = "- %s: " % tenant.name
    if len(tenant.utilities.keys()) > 1:
        line += string.join([fmoney.format(u) for u in tenant_utils], " + ")
        line += " = "
    line += fmoney.format(tenant.paid())
    print line

print ""

print "Total paid for all utilities: " + fmoney.format(total_utilities)

print ""

print "Each of us individually owes: " + fmoney.format(tenant_owes)

print ""

print "What each of us owes - what each of us paid = remaining amount owed:"

for tenant in tenants:
    print f.format("{0}: {1:$,.2f} - {2:,.2f} = {3:$,.2f}",
                   tenant.name,
                   tenant.owes,
                   tenant.paid(),
                   tenant.owes - tenant.paid()
                   )
