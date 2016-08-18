 Our goal was to make it easy for researchers to use more realistic networks on GENI. With more realistic networks to test on, researchers should be able to make advancements that have a better impact on more Americans' internet. Our result is a Python script that looks up representative network information in a data set of real home Internet measurements, and produces an output file that researchers can then use to test their networking ideas on a link that emulates that specific home.

### Issue

* There exists a digital divide between web developers and internet users in the United States.

### Problem

* Internet researchers and developers don't do tests on realistic links.
* Some tests are done directly connected to university networks, which have much better speeds than most home users.  
* Some tests are done on GENI, where the default link speed is much higher than most US households' download speed.
* Many researchers do not change link characteristics on test setup to something more realistic.


### So What

* Advancements may not work as intended for the millions of Americans who have different Internet speeds.
* When developers _do_ test on realistic connections (like at Facebook), they create applications that offer a better experience to a wide range of users.


### Solutions

* Our goal was to make it easy for researchers to use more realistic networks on GENI.
* We used a dataset of measurements from the Measuring Broadband America program
* We made a Python script that samples a household from this dataset, and finds the measurements of that household's Internet connection
* Researchers using our tool can also specify a input to focus on a specific target group
* Our tool generates a setup on GENI where the link matches the sampled household
* Our tool also generates a profile that can be used with ATC
* Depending on how much control they need to have over the network and the endpoints, researchers may prefer one solution or the other.
 
### Benefits

* This tool can help researchers design more effective developements for everybody.
