# DS-Tools
Classifiers and scripts made for my Data-Science course

## Weka Classifiers

### Set-up
A few steps had to be taken in order to be able to add my custom Weka classifier to the program and display. To start, I had to demonstrate the ability to compile and build from Weka's source code (I'm on Linux but I don't the process changes much). This may be acquired at the [mirror](https://github.com/Waikato/weka-3.8) on GitHub or through other channels documented such as [SourceForge](https://sourceforge.net/projects/weka/files/weka-3-8/3.8.4/weka-3-8-4-azul-zulu-linux.zip/download?use_mirror=pilotfiber) (I recommend the latter for reasons we'll get to later). The links I have are for the most up-to-date versions at the time of writing (March 2020).   
After referencing the Weka documentation, there were a few options served: use Ant, Maven, or an IDE such as IntelliJ/Netbeans/Eclipse. I decided to try Netbeans, against my better judgement. After hours of only complete and total failure(s), I decided to try out the Ant method:  

```
# wd: $HOME/weka-$RELEASE/weka/ for GitHub clone
# wd: $HOME/weka-3-8-4-azul-zulu-linux/weka-$RELEASE/ for SourceForge download
$ ant -f build.xml exejar
```
This finally worked and created the new `weka.jar` file in the newly-created `dist` directory. I copied this file over to my directory containing the `weka.sh` script and everything came up. 

### Custom Classifier
Time to begin the fun! I want to demonstrate the ability to add my own classifier to Weka. This topic is covered in the blog link below, however I will give a brief overview here.  
I had to find a classifier to mimic for the time being (since this is purely a PoC currently). I chose the `InputMappedClassifier`, found at `weka.classifiers.misc` (or `weka/src/main/java/weka/classifiers/misc`). I created a copy of this classifier named it `HelloWorld` (make sure to change the class name **and** the file name if you're not familiar enough with java). An additional step required is to add this file to the `GenericObjectEditor.props` file found in `weka/gui`. Also, make sure that the `UseDynamic` flag is set to `true` in the `GenericPropertiesCreator.props` file, otherwise your custom classifiers will not be loaded.  
Once all of this is finished, we can compile Weka just like before and re-run the `weka.sh` script. In the image here, we can see the image of the Weka classifiers. 

![image of HelloWorld classifier in the Weka misc classifier list](https://github.com/JohnsonClayton/DS-Tools/blob/master/media/hw_added.png)

*I am unsure why my former "SeriousTest" classifier is present, I must investigate this further.*


## References
1. Weka Documentation (https://waikato.github.io/weka-wiki/ant/)
2. Weka Blog (https://waikato.github.io/weka-blog/posts/2018-10-08-making-a-weka-classifier/)
