How the UI WORKS 
IMPORTING 
	For this you need to have two datasets, must be CSV and one configuration file with the same 
	Structure as provided. 
		- for the two csv files make sure that they have the same amount of entries for the columns unless 
		  taking the difference will not work 
		- also make sure that the column names is specified correctly in the configuration file.
REVIEW:
	Make sure there are no empty fields and that ":" character is used to deliminate when we finished with the text 
		e.g.: Max Tank Value: 10 
	Also make sure that numbers are inputed after ":". While you can have letters and text if there are no numbers then you will 	encounter an error 
Source Code
	Tank/containers:
		- this is the tank/container class object that contains various information regarding tanks such as max min, ect 
		
		- these need to be initalized after the UI has finished as they will be used for the optimalization 
	System Initalization:
		- All this does is take the critical information from the configuration and datasets and assigns them along with
		  creating the tanks and containers classes
	Optimal Tanks:
		- this goes through and determines wether we need to create a tank or have a tank already created that can store the 		  energy or has enough energy to drain to meet the demands
		- This is primarily done thorugh comparing the currentChargedCapacity() of the tank for discharging. And the 		          remainingCapacity() For charging
		- if we can store everything in a tank or tanks then we are good otherwise create a new tank
		- also need to stop creating and storing energy if we have met the energy demands
	Optimal Containers:
		- Works very simmilarly to the Tanks and requires the tanks to be created before this can occure
		- uses the Containers,to get the critical information including charge and current charge of the contaienr
		- though it needs to connect the containers with the tanks along with determinining which sections containers belong 		  to as well. 
	getDataContainer/Tank:
		- essentailly running through and draining and charging where needed and recording this change in an array to later 		  be put into a dictionary in the expanded graphs UI to create a graph of the data.
		- this requires both optimal containers and tanks to be completed so that they can run through and simulate the 		  draining and charging for recroding 