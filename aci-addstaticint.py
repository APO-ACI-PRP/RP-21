#!/usr/bin/env python

from acitoolkit.acitoolkit import *
import re
import sys


def selectTenant(session):
    """ Returns an ACI toolkit tenant object after interacting with the user. """
    tenantList = Tenant.get(session)
    tenants = {}
    for tenant in tenantList:
        print tenant.name
        tenants[tenant.name] = tenant
    selection = raw_input('What tenant would you like to work with? ')
    # print selection
    return tenants[selection]

def selectEPG(session, tenant):
    appProfiles = AppProfile.get(session, tenant)
    epgs = {}
    for ap in appProfiles:
        for epg in EPG.get(session, ap, tenant):
            epg.populate_children(True,True)
            epg_app = "%s/%s" % (ap.name, epg.name)
            epgs[epg_app] = epg
    if len(epgs) == 0:
        print "Tenant %s has no End Point Groups, exiting." % tenant.name
        sys.exit(1)
        # return None
    print "EPGs: "
    for ea in sorted(epgs.keys()):
        print ea
        #print epgs[ea].get_interfaces()
    selection = raw_input("Which AppProfile/EPG would you like? ")
    return epgs[selection]



def updateInterfaces(session, epg):
    temp = raw_input("Enter the interface range to update [ie 1/101/1/1-30]: ")
    [pod, leaf, swmod, intRange] = temp.split('/')
    if re.match('.*-.*', intRange) != None:
        [startInt, stopInt] = intRange.split('-')
    else:
        startInt = intRange
        stopInt  = intRange
    vlan = int(raw_input("Enter the VLAN # to use: "))
    startInt = int(startInt)
    stopInt  = int(stopInt)
    if startInt > stopInt:
        print "Start interface must be <= stop interface in range"
    i = startInt
    while i <= stopInt:
        intf = Interface('eth',pod,leaf,swmod, str(i))
        L2intf = L2Interface("vlan%d_on_interface_%d" % (vlan,i), 'vlan', str(vlan) )
        L2intf.attach(intf)
        epg.attach(L2intf)
        i = i + 1
    return epg


def main():
    description = ('LANs test tenant')
    creds = Credentials('apic',description)
    args = creds.get()

    session = Session(args.url, args.login, args.password)
    session.login()

    tenant = selectTenant(session)
    # print tenant
    epg = selectEPG(session, tenant)
    # epg = getEndPointGroupsByTenant(session, tenant)
    epg = updateInterfaces(session, epg)
    # print epg.get_json()
    # print tenant.get_json()
    # print epg
    # print type(epg)
    resp = session.push_to_apic(tenant.get_url(), data=tenant.get_json())
    if resp.ok:
        print "Success"
    else:
        print "Error: "
        print resp.reason

    # print EPG.get_children()
    # print tenants

    # eps = filterEndPointsByTenant(getEndPoints(session), "OSO-Lab")
    # for ep in eps:
    #     print ep.get_parent().get_parent().get_parent().name + ep.name
    # print getEndPointGroups(session)
    # print getEndPointGroupsByTenant(session, Tenant("OSO-Lab"))


def buildTenant():
    tenant = Tenant('LAN-tenant')
    app    = AppProfile('LAN-appProfile', tenant)
    epg    = EPG('LAN-epg', app)
    vrf    = Context('LAN-vrf', tenant)
    bd     = BridgeDomain('LAN-bd', tenant)

    bd.add_context(vrf)
    epg.add_bd(bd)

    intf1 = Interface('eth','1','101','1','30')
    vlan200_on_intf1 = L2Interface('vlan200_on_intf1','vlan','200')
    vlan200_on_intf1.attach(intf1)
    epg.attach(vlan200_on_intf1)

    description = ('LANs test tenant')
    creds = Credentials('apic',description)
    args = creds.get()

    session = Session(args.url, args.login, args.password)
    session.login()

    resp = session.push_to_apic(tenant.get_url(), data=tenant.get_json())
    if resp.ok:
        print "Success"
    else:
        print resp.status_code
        print resp.reason

if __name__ == "__main__":


    # buildTenant()
    main()
