#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: David Espejo (Fortytwo Security)
import argparse
import dns.query
import dns.zone
import dns.resolver

def perform_zone_transfer(domain, ns_servers):
    for ns_server in ns_servers:
        print(f"Attempting zone transfer with {ns_server} for domain {domain}...")
        
        try:
            # Perform the zone transfer
            zone = dns.zone.from_xfr(dns.query.xfr(ns_server, domain))
            print(f"Zone transfer successful with {ns_server} for domain {domain}")
            
            # Print the records
            for name, node in zone.nodes.items():
                rdatasets = node.rdatasets
                for rdataset in rdatasets:
                    print(f"{name} {rdataset}")
        except Exception as e:
            print(f"Zone transfer failed with {ns_server} for domain {domain}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform DNS Zone Transfers")
    parser.add_argument("-d", "--domains", required=True, help="Comma-separated list of domains to transfer")
    parser.add_argument("-s", "--servers", required=True, help="Comma-separated list of DNS servers to use")
    args = parser.parse_args()
    
    domains = args.domains.split(",")
    ns_servers = args.servers.split(",")
    
    for domain in domains:
        perform_zone_transfer(domain.strip(), [server.strip() for server in ns_servers])
