/*
 * Clayton Johnson
 * CSCI-396 : Introduction to Data Science
 * Dr. Sherine Antoun
 *
 * PRISM 
 *  Algorithm presented in "PRISM: An algorithm for inducing modular rules" by Jadzia Cendrowska (1987)
 *
*/


package weka.classifiers.rules;

import weka.classifiers.Classifier;
import weka.classifiers.AbstractClassifier;
import weka.core.Attribute;
import weka.core.Capabilities;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.RevisionHandler;
import weka.core.RevisionUtils;
import weka.core.TechnicalInformation;
import weka.core.TechnicalInformationHandler;
import weka.core.Capabilities.Capability;
import weka.core.TechnicalInformation.Field;
import weka.core.TechnicalInformation.Type;
import weka.core.Utils;

import java.io.Serializable;
import java.util.Enumeration;

public class PRISM extends AbstractClassifier {

	public void buildClassifier(Instances trainingData) throws Exception {
				

	}

	public double classifyInstance(Instance instance) {
		return 1.0;
	}

	public String toString() {
		return "PRISM implemented by Clayton Johnson";
	}

}
