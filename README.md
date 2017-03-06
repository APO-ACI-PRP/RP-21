# Rotation #21 ANM
nx-api-class.py - Nexus health check tool. Our script looks for flapping routes, STP TCNs, and instances of dynamic routing across a VPC peer link.
aci-addstaticint.py - This script prompts for a Tenant and EPG, and then a range of interfaces to be configured as static ports. We also a script to create contracts. Both scripts use the ACI toolkit.
aci-mkcontract.py - I created a script used to create contracts. It took input from customer on TCP port # and gave a list of tenants to choose from. The idea of this script was to be able to push contracts to separate ACI domains
