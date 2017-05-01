"""Summary
"""
import pandas as pd

class HouseholdSet(object):

    def __init__(self, path):

        self.data = pd.read_csv(path)

    def sample(self):

        return self.data.sample(n=1, weights=self.data.weight)

    def sample_n(self, nusers):

        return self.data.sample(n=nusers, weights=self.data.weight)


class Household(object):
    """Summary

    Attributes:
        advertised_rate_down (TYPE): Description
        advertised_rate_up (TYPE): Description
        isp (TYPE): Description
        jitter_down_ms (TYPE): Description
        jitter_up_ms (TYPE): Description
        latency_ms (TYPE): Description
        loss (TYPE): Description
        monthly_charge (TYPE): Description
        rate_down_kbps (TYPE): Description
        rate_up_kbps (TYPE): Description
        state (TYPE): Description
        technology (TYPE): Description
        unit_id (TYPE): Description
    """
    def __init__(self, h):
        """Summary

        Args:
            h (TYPE): Description
        """
        self.unit_id = h.get_value('unit_id')
        self.loss = h.get_value('medianLoss')
        self.latency_ms = h.get_value('medianLatency')/1000.0
        self.jitter_up_ms = h.get_value('medianJitterUp')/1000.0
        self.jitter_down_ms = h.get_value('medianJitterDown')/1000.0
        self.rate_up_kbps = h.get_value('medianUp') * 0.008
        self.rate_down_kbps = h.get_value('medianDown') * 0.008
        self.advertised_rate_up = h.get_value('advertised.up')
        self.advertised_rate_down = h.get_value('advertised.down')
        self.state = h.get_value('state')
        self.isp = h.get_value('isp')
        self.monthly_charge = h.get_value('monthly.charge')
        self.technology = h.get_value('technology')

    def netem_template_up(self, ip_address_str):
        """Summary

        Args:
            ip_address (TYPE): Description

        Returns:
            TYPE: Description
        """
        statements = [
            "sudo tc qdisc add dev %s root handle 1:0 tbf rate %dkbit limit 500000000 burst 100000" % (ip_address_str, self.rate_up_kbps),
            "sudo tc qdisc add dev %s parent 1:1 handle 10: netem delay %0.6fms %0.6fms loss %0.6f%%" % (ip_address_str, self.latency_ms/2.0, self.jitter_up_ms, self.loss/2.0)
        ]
        return "; ".join(statements)

    def netem_template_down(self, ip_address_str):
        """Summary

        Args:
            ip_address (TYPE): Description

        Returns:
            TYPE: Description
        """
        statements = [
            "sudo tc qdisc add dev %s root handle 1:0 tbf rate %dkbit limit 500000000 burst 100000" % (ip_address_str, self.rate_down_kbps),
            "sudo tc qdisc add dev %s parent 1:1 handle 10: netem delay %0.6fms %0.6fms loss %0.6f%%" % (ip_address_str, self.latency_ms/2.0, self.jitter_down_ms, self.loss/2.0)
        ]
        return "; ".join(statements)

    def truth_template(self):
        """Summary

        Returns:
            TYPE: Description
        """
        return [
            ["type", "measure"],
            ["ulrate", self.rate_up_kbps],
            ["dlrate", self.rate_down_kbps],
            ["latency", self.latency_ms],
            ["uljitter", self.jitter_up_ms],
            ["dljitter", self.jitter_down_ms],
            ["loss", self.loss]
        ]

    def json_template(self):
        """Summary

        Returns:
            TYPE: Description
        """
        json = {
            "content": {
                "down": {
                    "corruption": {
                        "correlation": 0,
                        "percentage": 0
                    },
                    "delay": {
                        "correlation": 0,
                        "delay": str(int(round(self.latency_ms/2.0))),
                        "jitter": str(int(round(self.jitter_down_ms)))
                    },
                    "iptables_options": [],
                    "loss": {
                        "correlation": 0,
                        "percentage": str(self.loss/2.0)
                    },
                    "rate": str(int(round(self.rate_down_kbps))),
                    "reorder": {
                        "correlation": 0,
                        "gap": 0,
                        "percentage": 0
                    }
                },
                "up": {
                    "corruption": {
                        "correlation": 0,
                        "percentage": 0
                    },
                    "delay": {
                        "correlation": 0,
                        "delay": str(int(round(self.latency_ms/2.0))),
                        "jitter": str(int(round(self.jitter_up_ms)))
                    },
                    "iptables_options": [],
                    "loss": {
                        "correlation": 0,
                        "percentage": str(self.loss/2.0)
                    },
                    "rate":str(int(round(self.rate_up_kbps))),
                    "reorder": {
                        "correlation": 0,
                        "gap": 0,
                        "percentage": 0
                    }
                }
            },
            "id": self.unit_id,
            "name": "house" + str(self.unit_id)
        }
        return json


    def print_house_info(self):
        """Summary

        Returns:
            TYPE: Description
        """
        print "\nSelected household %d has the following characteristics:" % self.unit_id
        print "Plan: %s/%s (Mbps down/up), %s (%s), %s" % (
            self.advertised_rate_down, self.advertised_rate_up,
            self.isp, self.technology, self.state)
        print "Estimated price per month: $%s" % self.monthly_charge
        print "--------------------------------------------------------"
        print " Upload rate (kbps)    | %d                             " % self.rate_up_kbps
        print " Download rate (kbps)  | %d                             " % self.rate_down_kbps
        print " Round-trip delay (ms) | %f                             " % self.latency_ms
        print " Uplink jitter (ms)    | %f                             " % self.jitter_up_ms
        print " Downlink jitter (ms)  | %f                             " % self.jitter_down_ms
        print " Packet loss (%%)       | %f                             " % self.loss
        print "--------------------------------------------------------"


class Star(object):
    """Summary

    Attributes:
        house_count (int): Description
        house_count_local (int): Description
        households (list): Description
        links (list): Description
        router (TYPE): Description
        server_count (int): Description
    """
    # class variables
    house_count = 0
    server_count = 0


    def __init__(self):
        """Summary
        """

        # Import optional libraries
        import geni.rspec.igext as IGX

        self.households = []
        self.router = IGX.XenVM("router-%d" % self.server_count)
        self.links = []
        self.house_count_local = 0

        self.server_count += 1

    def add_household(self, house):
        """Summary

        Args:
            house (TYPE): Description

        Returns:
            TYPE: Description
        """

        # Import optional libraries
        import geni.rspec.pg as PG
        import geni.rspec.igext as IGX

        speed = max(house.rate_up_kbps, house.rate_down_kbps)
        self.links.insert(self.house_count_local, PG.LAN('lan%d' % self.house_count))
        self.links[self.house_count_local].bandwidth = int(speed)

        igvm = IGX.XenVM("house-%d" % house.unit_id)

        ip_netem = "10.0.%d.0" % self.house_count
        netem_str = "$(ip route get %s | head -n 1 | cut -d \  -f4)" % (ip_netem)
        user_netem = house.netem_template_up(netem_str)
        server_netem = house.netem_template_down(netem_str)

        self.router.addService(PG.Execute(shell="/bin/sh", command=server_netem))
        igvm.addService(PG.Execute(shell="/bin/sh", command=user_netem))
        self.households.insert(self.house_count_local, igvm)

        iface = igvm.addInterface("if-%d-1" % self.house_count)
        iface.addAddress(PG.IPv4Address("10.0.%d.1" % self.house_count, "255.255.255.0"))
        self.links[self.house_count_local].addInterface(iface)

        server_iface = self.router.addInterface("if-%d-2" % self.house_count)
        server_iface.addAddress(PG.IPv4Address("10.0.%d.2" % self.house_count, "255.255.255.0"))
        self.links[self.house_count_local].addInterface(server_iface)

        self.house_count_local += 1
        self.house_count += 1

    def add_validate_services(self):
        """Summary

        Returns:
            TYPE: Description
        """

        # Import optional libraries
        import geni.rspec.pg as PG

        kernel_tuning = """sudo sysctl -w net.core.rmem_max=134217728;
                           sudo sysctl -w net.core.wmem_max=134217728;
                           sudo sysctl -w net.ipv4.tcp_rmem='4096 87380 67108864';
                           sudo sysctl -w net.ipv4.tcp_wmem='4096 65536 67108864'"""
        iperf_setup = "wget -qO- https://raw.githubusercontent.com/csmithsalzberg/digitaldivide/master/util/iperfsetup.sh"

        wget_validate = "wget -O /tmp/validate.sh https://raw.githubusercontent.com/csmithsalzberg/digitaldivide/master/util/validate.sh"
        wget_consolidate = "wget -O /tmp/consolidate-validation-results.sh https://raw.githubusercontent.com/csmithsalzberg/digitaldivide/master/util/consolidate-validation-results.sh"

        self.router.addService(PG.Execute(shell="/bin/sh", command="%s | bash; iperf3 -s -D; iperf -s -u" % iperf_setup))
        self.router.addService(PG.Execute(shell="/bin/sh", command=kernel_tuning))

        for house in self.households:
            house.addService(PG.Execute(shell="/bin/sh", command="%s | bash" % iperf_setup))
            house.addService(PG.Execute(shell="/bin/sh", command=wget_consolidate))
            house.addService(PG.Execute(shell="/bin/sh", command=wget_validate))

    def rspec_template(self, rspec):

        """Summary

        Args:
            rspec (TYPE): Description

        Returns:
            TYPE: Description
        """

        rspec.addResource(self.router)
        for house in self.households:
            rspec.addResource(house)
        for link in self.links:
            rspec.addResource(link)
        return rspec

    def rspec_write(self, rspecfile):
        """Summary

        Args:
            rspecfile (TYPE): Description

        Returns:
            TYPE: Description
        """

        # Import optional libraries
        import geni.rspec.pg as PG

        r = PG.Request()
        self.rspec_template(r)
        r.writeXML(rspecfile)
