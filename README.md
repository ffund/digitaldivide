## Background

 There exists a digital divide between web developers and internet users in the United States. Some households do not have high-speed Internet avavilable in their area, or cannot pay for high-speed Internet. As a result, there is a lot of variation in Internet speed across households in the US. We see this in the image below, which shows the relative frequency of different download speeds of US households. Meanwhile, web developers and researchers usually have top-notch internet connections. This disparity is called the "digital divide".
 
 ![varying speeds graph](https://github.com/csmithsalzberg/CodeRealisticTestbeds/blob/master/percentDLwithColor.png) 
 
 Internet researchers and developers mainly use high-speed home or university Internet connections to test new ideas, or they use dedicated infrastructure called "testbeds" that have good quality links [1]. Sometimes they use a single device, or a small sample of machines to run tests, but these tests are done directly connected to university networks, which have much better speeds than most home users [2].  
 
 Alternatively, researchers may use a platform called GENI to test developments on dedicated research infrastructure. When using GENI, reseachers use a web-based interface in which virtual machines (VMs) can be dragged onto the canvas area, and connected by links (as show in the screenshot below) [3]. These virtual machines and links are then reserved at one of a set of server racks at universities across the US, and researchers can log into each of the virtual machines, install networked applications, and use them and measure their performance. However, the default link speed on GENI is 100 megabits per second, which we see in the image above is much higher than most US households' download speed. Also, default latency and packet loss on GENI is minimal, which does not at all similar to real household network connections. 
 
  ![GENI portal](https://github.com/csmithsalzberg/CodeRealisticTestbeds/blob/master/geniexample.PNG) 

Characteristics such as download speed, upload speed, latency, jitter, and packet loss, _can_ be changed on GENI. However, many researchers do not change these to something more realistic. If researchers do not deliberately change characteristics of the link to match their target users' network characteristics, the network that they test on will not accurately represent real households.

When developers and researchers do not test their ideas on a variety of realistic networks, their advancements may not work as intended for the millions of Americans who have different Internet speeds. Companies like Facebook recognize the importance of this. Facebook instituted a program called "2G Tuesdays" where employees have the option of using low-quality Internet speeds similar to that of the developing world, in order to get a better understanding of how people with worse internet speeds experience their applications [4]. This experiment actually had a big impact on the Facebook team, and they have said that it led them to change the way parts of the Messenger app work to better support users in emerging markets.
 
 
 Our goal was to make it easy for researchers to use more realistic networks on GENI. With more realistic networks to test on, researchers should be able to make advancements that have a better impact on more Americans' internet. Our result is a Python script that looks up representative network information in a data set of real home Internet measurements, and produces an output file that researchers can then use to test their networking ideas on a link that emulates that specific home.
 
 We used a dataset of measurements from the Measuring Broadband America program [5]. This is a program by the FCC to gather information on the Internet quality of US households. Volunteer panelists get a wireless router through which they connect to the Internet using their regular Internet plan provided by their own Internet service provider (ISP). The router automatically runs network tests every hour and reports measurements back to the FCC. The panelists have a range of Internet service plans, of different types (cable, satellite, fiber, DSL), from different ISPs, and paying different prices for different upload and download speeds. They also come from different locations around the US. Potential panelists are selected so that the measurements give information about all the different kinds of Internet service plans available in the US.
 
 The tool we created is a Python script that samples a random household from this dataset, and finds the measurements of that household's Internet connection in the data set. Researchers using our tool can also specify as input the state, price range, and/or technology so as to limit their outputs to households that represent a target group. For example, if a researcher is trying to make an application specifically for lower income communities, then the researcher would most likely search for a household paying a low price. The map below shows examples of households across the United States, paying different prices, with different ISPs, and in states with different average Internet speed, as a demonstration of the range of households researchers can emulate in their tests:
 
  ![map](https://github.com/csmithsalzberg/CodeRealisticTestbeds/blob/master/mapwithheat.png) 

Once an actual household is selected from the dataset, the information from the household can be used in two ways. Our code generates a "resource specification" (RSpec) file that can be used directly to create a small network on GENI. In the network, one VM represents the user, and the other represents the server (as shown in the image below). The link between the user and the server has the same qualities - upload speed, download speed, latency, jitter, and packet loss - as the selected household. The researchers can then log in to the VMs and run experiments over that link, which represents a real US household.

![GENI topology](https://github.com/csmithsalzberg/CodeRealisticTestbeds/blob/master/GENIposter.PNG) 

Our tool also generates a profile that can be used in Augmented Traffic Control (ATC), which is the technology developed by Facbeook for programs like "2G Tuesdays". With ATC, a researcher tunnels the network traffic from their own laptop or phone through a link on GENI, and browses the Internet or use apps through that link [6]. Using a browser-based UI (shown in the image below), researchers can make that link through which their traffic travels have specific characteristics. Our tool generates an ATC profile that can be applied to the tunneled traffic, so that it has the qualities of the sampled US household.

![ATC](https://github.com/csmithsalzberg/CodeRealisticTestbeds/blob/master/profiles.PNG) 

Depending on how much control they need to have over the network and the endpoints, researchers may prefer one solution or the other. Because there are no outside factors involved, the first approach using links and end hosts only on GENI allows researchers to test advancements in  a very controlled environment. The second method includes outside influences, since in addition to going through the GENI link the traffic also goes over the regular Internet. Also, researchers do not have total control over the end hosts. But, with ATC you can use graphical applications, like a regular web browser, and you can also include external factors like load on the target server.


We hope that the GENI network and the internet profile our tool generates will have an impact on researchers.  If a new advancement is tested on multiple households, researchers will get a better idea whether or not their application works under different circumstances. Our ultimate goal is for this tool to help researchers design more effective developements for everybody.
 

## Run my experiment

Download "full.csv" from my repository

Download "finalexperiment.py" from src/ and put it in a subdirectory to full.csv (one level lower than full.csv)

Next, follow instructions [here](https://www.continuum.io/downloads), to download Anaconda

Follow [this tutorial](https://witestlab.poly.edu/respond/sites/genitutorial/module/introduction-testbeds) to learn how to use GENI

Install [geni-lib](https://geni-lib.readthedocs.io/en/latest/intro/install.html)
 
Run the script from the directory with full.csv in it: python finalexperiment.py

If you want to filter by state, technology, or price range: python finalexperiment.py --state (two letter code) --houseid (any number, but database doesn't include most) --price_range min-max --Technology (CABLE, FIBER, or DSL)

The output should look something like this: 
<pre>
for user:
sudo tc qdisc add dev eth1 root handle 1:0 netem delay 9.2172741821ms 3.00476386913ms loss 0.0286073654638%
sudo qdisc add dev eth1 parent 1:1 handle 10: tbf rate 1058kbit limit 500000000 burst 100000
for server:
sudo tc qdisc add dev eth1 root netem delay 9.2172741821ms 2.43315504979ms loss 0.0286073654638%
sudo tc qdisc add dev eth1 parent 1:1 handle 10: tbf rate 15778kbit limit 500000000 burst 100000
Rspec written to file
{
    "content": {
        "down": {
            "corruption": {
                "correlation": 0,
                "percentage": 0
            },
            "delay": {
                "correlation": 0,
                "delay":"9.2172741821",
                "jitter":"2.43315504979"
            },
            "iptables_options": [],
            "loss": {
                "correlation": 0,
                "percentage":"0.0286073654638"
            },
            "rate":"15778",
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
                "delay":"9.2172741821",
                "jitter":"3.00476386913"
            },
            "iptables_options": [],
            "loss": {
                "correlation": 0,
                "percentage":"0.0286073654638"
            },
            "rate":"1058",
            "reorder": {
                "correlation": 0,
                "gap": 0,
                "percentage": 0
            }
        }
    },
    "id": 10,
    "name": "house8334"
}
</pre>

#Use GENI to model the specified household's netowork characteristics

Now, log into GENI and create a new slice

Next you want to copy the contents of miniexperiment.xml and place it in the textbox on the GENI interface. A two node topology should pop up.

Log into both the nodes using ssh.

Run the two commands under "user" on the node titled user and the two commands under "server" on the node titled server.

Those nodes are then set up and ready with the correct characteristics.

#Using ATC to model the specified household's netowork characteristics

Follow instructions [here](https://witestlab.poly.edu/blog/2g-tuesdays-emulating-realistic-network-conditions-in-emerging-markets/) to set up the ATC web browsing part of the experiment.

Test that you have everything set up correctly by browsing under the provided profiles to check that the internet is being shaped

Once finished with that: cd ~/augmented-traffic-control/utils/profiles on an openvpn node

Add a new file titled (anything).json and copy the contents under "Rspec written to file" and ending with "}" to the new file in profiles.

run: cd .. 

and then run: bash restore-profiles.sh localhost:8000 

Refresh http://10.8.0.1:8000, and you should see your new profile

Select that profile, and surf the web on the proxied tab. You are now using an internet connection modelled by the sampled household!

Thank you for participating!

## Citations

[1] Muhammad, Monzur, and Justin Cappos. "Towards a representive testbed: Harnessing volunteers for networks research." The First GENI Research and Educational Workshop, GREE. Vol. 12. 2012. [https://isis.poly.edu/~jcappos/papers/muhammad_seattle_geni_12.pdf](https://isis.poly.edu/~jcappos/papers/muhammad_seattle_geni_12.pdf)

[2] Yung-Chih Chen, Don Towsley, and Ramin Khalili. 2014. MSPlayer: Multi-Source and multi-Path LeverAged YoutubER. In Proceedings of the 10th ACM International on Conference on emerging Networking Experiments and Technologies (CoNEXT '14). ACM, New York, NY, USA, 263-270. DOI=http://dx.doi.org/10.1145/2674005.2675007 

[3] [GENI site](https://www.geni.net/)

[4] Fund, Fraida. "2G Tuesdays: Emulating Realistic Network Conditions in Emerging Markets." Run My Experiment on GENI. N.p., July-Aug. 2016. Web. 2016. [https://witestlab.poly.edu/blog/2g-tuesdays-emulating-realistic-network-conditions-in-emerging-markets/](https://witestlab.poly.edu/blog/2g-tuesdays-emulating-realistic-network-conditions-in-emerging-markets/)

[5] "2015 Measuring Broadband America Fixed Report." Federal Communications Commission. N.p., 2015. Web. 2016. [https://www.fcc.gov/reports-research/reports/measuring-broadband-america/measuring-broadband-america-2015](https://www.fcc.gov/reports-research/reports/measuring-broadband-america/measuring-broadband-america-2015)

[6] "Augmented Traffic Control: A Tool to Simulate Network Conditions." Facebook Code. N.p., n.d. Web. 01 Aug. 2016. [https://code.facebook.com/posts/1561127100804165/augmented-traffic-control-a-tool-to-simulate-network-conditions/](https://code.facebook.com/posts/1561127100804165/augmented-traffic-control-a-tool-to-simulate-network-conditions/)


