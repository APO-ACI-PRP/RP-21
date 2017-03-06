#!/usr/bin/python

from acitoolkit.acitoolkit import Credentials, Session, Tenant, FilterEntry
from acitoolkit.acitoolkit import Contract
import acitoolkit.acitoolkit as ACI
import sys



def main(name,session):

    tenant = Tenant(name)
    conname = raw_input("Enter a name for the contract: ")
    portnum = raw_input("Enter TCP port number: ")

    contract1 = Contract(conname,tenant)
    entry1 = FilterEntry(conname,
                         applyToFrag='no',
                         arpOpc='unspecified',
                         dFromPort=portnum,
                         dToPort=portnum,
                         etherT='ip',
                         prot='tcp',
                         sFromPort='1',
                         sToPort='65535',
                         tcpRules='unspecified',
                         parent=contract1)


    resp = session.push_to_apic(tenant.get_url(),tenant.get_json())

def tenant(session):

    # Print all of the tenants
    print("TENANT")
    print("------")
    tenants = ACI.Tenant.get(session)
    i=0
    for tenant in tenants:
        print str(i) +": " + (tenant.name)
        i += 1
    tenantname = raw_input("Input the # for the tenant you want: ")

    finalname = tenants[int(tenantname)]
    print finalname
    return str(finalname)

def creds():
    creds = Credentials('apic')
    args = creds.get()
    session = Session(args.url, args.login, args.password)
    session.login()
    return session

if __name__ == '__main__':
    apic = creds()
    tenantname = tenant(apic)
    main(tenantname,apic)
