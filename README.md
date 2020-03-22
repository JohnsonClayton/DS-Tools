# DS-Tools
Classifiers and scripts made for my Data-Science course

## Weka Classifiers

### Set-up
A few steps had to be taken in order to be able to add my custom Weka classifier to the program and display. To start, I had to demonstrate the ability to compile and build from Weka's source code (I'm on Linux but I don't believe the process changes much). This may be acquired at the [mirror](https://github.com/Waikato/weka-3.8) on GitHub or through other channels documented such as [SourceForge](https://sourceforge.net/projects/weka/files/weka-3-8/3.8.4/weka-3-8-4-azul-zulu-linux.zip/download?use_mirror=pilotfiber) (I recommend the latter for reasons we'll get to later). The links I have are for the most up-to-date versions at the time of writing (March 2020).   
After referencing the Weka documentation, there were a few options served: use Ant, Maven, or an IDE such as IntelliJ/Netbeans/Eclipse. I decided to try Netbeans, against my better judgement. After hours of only complete and total failure(s), I decided to try out the Ant method. Below, I have displayed the working directory (wd, just the directory this build command is run in. This will depend on how you installed Weka). The `ant` command should come with any JDK/JRE install, however it *may* have to be downloaded. This is run in the terminal. 

```
NOTE  
wd: $HOME/weka-$RELEASE/weka/ for GitHub clone
wd: $HOME/weka-3-8-4-azul-zulu-linux/weka-$RELEASE/ for SourceForge download
$ ant -f build.xml exejar
```
This finally worked and created the new `weka.jar` file in the newly-created `dist` directory. I copied this file over to my directory containing the `weka.sh` script and everything came up. 

### Custom Classifier
Time to begin the fun! I want to demonstrate the ability to add my own classifier to Weka. This topic is covered in the blog link below, however I will give a brief overview here.  
I had to find a classifier to mimic for the time being (since this is purely a proof of concept, currently). I chose the `InputMappedClassifier`, found at `weka.classifiers.misc` (or `weka/src/main/java/weka/classifiers/misc`). I created a copy of this classifier named it `HelloWorld` (make sure to change the class name **and** the file name if you're not familiar enough with java). An additional step required is to add this file to the `GenericObjectEditor.props` file found in `weka/gui`. Also, make sure that the `UseDynamic` flag is set to `true` in the `GenericPropertiesCreator.props` file, otherwise your custom classifiers will not be loaded.  
Once all of this is finished, we can compile Weka just like before and re-run the `weka.sh` script. In the image here, we can see the image of the Weka classifiers. 

![image of HelloWorld classifier in the Weka misc classifier list](https://github.com/JohnsonClayton/DS-Tools/blob/master/media/hw_added.png)

*I am unsure why my former "SeriousTest" classifier is present, I must investigate this further.*

### Running the Classifier (CLI)
In order to run a given classifier from the Terminal (or CLI), the following steps may be required:
```
$WEKA_PATH is the path to your Weka installation, mine is ~/.../weka-3.8/weka/
$ export CLASSPATH=$WEKA_PATH/weka.jar  

This is just an example of what I'm doing. Yours may be in different subdirectories
$ javac $WEKA_PATH/src/main/java/weka/classifiers/lazy/IB1.java 

Running the classifier
$ java weka.Run weka.classifiers.lazy.IB1.java -t ~/$DATA_PATH/breast-cancer.arff

```

You can always add the `-h` flag at the end of these commands to receive some help. Additional help may be found in the CLI Documentation link below.

### Automation of Tests
Since I have quite a few tests to run, I've created the `generate_data` and `run_all` bash scripts to automate this process. Below is an example of what is run in the data script:
```
for noise in {0..20} ; do
  file="./$dir/temp$noise.arff"
  rm $file 2> /dev/null
  ./LED 1000 $seed $file $noise >> /dev/null
  data="$(cat $file)"
  echo -e "$header\n$data" > $file
done
```
This snippet above will run through the ranges of noise desired for testing. In my case, I am running tests on data from 0-20% noise within the data. Additionally, this script will create (or overwrite) a directory to add all of these files to. The file naming works as `temp0.arff`, where temp can be whatever name and the 0 refers to the percentage of noise introduced by the `LED` program. The `arff` file is automatically prepended with the header information required.   
The next step would be to hand this information to the classifiers dynamically to require as minimal effort on my part as possible. Considering that there are 20 datasets (0-20% noise with step sizes = 1) and 10 different seeds (1-10) for the three classifiers (IB1, IB2, IB3), there are 600 tests required. The bash script line below is an example of how I am running and filtering the output data from Weka's CLI to improve the efficiency of this process:
```
$ java weka.Run weka.classifiers.lazy.IB1 -t $datafile$noise.arff -s $rand 2>/dev/null | grep -E "Correctly Classified Instances|IB1 Classifier" >> $outfile
```
This line is in two loops, the inner-most over the seeds and the outer-most over the noise levels. I could just as easily add the extra layer to dynamically call all three classifiers, however I figured this was fancy enough.  
*I recommend caution using this script* because I created it with the intention of executing it and walking away. If you run the script and know you need to stop it at some point, do not kick it off in the background. This will force you to either wait for all 600 `java` processes to terminate or chase them all down. *Just be advised* that if you mess something up on your machine, I warned you.

### Parsing Classifier Data
Currently, I am parsing the output of the automated tests with the `ib-processing` python script. The goal of the script is to automatically parse through the troves of data collected from the classifiers and to graph it. I am currently only collecting and parsing the accuracy data; however, in the future I will collect data on the number of instances saved from the training data.
```
classifiers.addDataToClassifier(current_classifier, noise_level, acc)
```
The data is parsed out into Classifier objects managed by a Classifiers object. This simplifies the process such that only one line is needed (see above) to hand the data to the classifier. The rest of the program keeps track of where we are in the output file. Once this is completed, I calculate the mean and standard deviation of all the IB1 data with 0% noise, then 1% noise, etc. for all of the classifiers. The graph generated is shown in the next section.

### Results and Discussion
Below is the graph showing the changes in the Instance-Based classifier performance as there is an increase in noise in the data set.

![Instance-Based Classifier Accuracy with Increasing Noise in Training Datasets](https://github.com/JohnsonClayton/DS-Tools/blob/master/media/ib1-3_accuracy.png)

The vertical lines represent the standard deviation of the model's accuracy at that level of noise introduced into the data set. As the models are presented, we see that there is little deviation between the IB1 and IB3 classifiers, while the IB2 classifier clearly has degraded in performance as there has been an increase in noise. In the next graph, we see the changes in memory required across the learners. IB1's memory usage doesn't change at all since its algorithm dictates that it save all the training instances. IB2 and IB3's memory are similar, with IB3 consistently saving more instances than IB2. 

![Instance-Based Classifier Accuracy with Increasing Noise in Training Datasets](https://github.com/JohnsonClayton/DS-Tools/blob/master/media/ib1-3_memory.png)
#### Does this make sense?
Let's compare the results to Aha's [5] results shown below.
![Aha's 1991 Results](https://github.com/JohnsonClayton/DS-Tools/blob/master/media/aha_results_1991.png)  
The left-most graph shows the performance of the instance-based learners over a larger range of introduced noise. Additionally, the data collected in this paper shows the mean over 50 runs of each learner as opposed to the 10 presented in this work. In the same noise range, we see similar results in that IB2 is the worst-performing out of the three. However, our results show IB1 outperforming IB3 (even if only slightly). Additionally, there is a clear distinction between IB2 and IB3 memory usage in Aha's paper while these results here show IB2 and IB3 performing similarly. These results are not in line with Aha's. 

In Aha's paper, they outline that the goal of IB3 is to improve noise tolerance and memory allowances. While all of my collected data isn't presented here yet, IB3 tolerates noise significantly better than IB2 and reduces the amount of instances saved from the training dataset by almost 50% compared to IB1, if only at a slight cost in performance. However, further data must be collected to demonstrate these advantages and to better compare the learners with Aha's results. 

While the implementation of IB3 presented here *may* be flawed or unrepresentative of the learner, the general ideas shown here are still true.  

## References
1. Weka Ant Documentation (https://waikato.github.io/weka-wiki/ant/)
2. Weka Blog (https://waikato.github.io/weka-blog/posts/2018-10-08-making-a-weka-classifier/)
3. CLI Documentation on SourceForge (https://prdownloads.sourceforge.net/weka/WekaManual-3-8-3.pdf?download)
4. General Documentation (https://waikato.github.io/weka-wiki/documentation/)
5. Aha, D., Kibler, D., Albert M., "Instance-based learning algorithms", Machine Learning, vol. 6, 1991, p. 37-66.
