/*
 * Clayton Johnson
 * CSCI-396 : Introduction to Data Science
 * Dr. Sherine Antoun
 *
 * PRISM 
 *  Algorithm presented in "PRISM: An algorithm for inducing modular rules" by Jadzia Cendrowska (1987)
 *
 *  Basic Algorithm:
 *	1. Calculate the probability of occurrence p(o_n | a_x) of the classification o_n for each attribute-value pair a_x
 *	2. Select the a_x for which p(o_n | a_x) is a maximum and create a subset of the training set comprising all the instances which contain the selected a_x
 *	3. Repeat steps 1-2 for this subset until it contains only instances of class o_n. The induced rule is a conjunction of all the attribute-value pairs used in creating the homogeneous subset.
 * 	4. Remove all instances covered by this rule from the training set.
 *	5. Repeat steps 1-4 until all instances of class o_n have been removed
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
import java.util.ArrayList;

public class PRISM extends AbstractClassifier {

	private class Rule {
		// Actions depend on the data type of the given relationship
		
	}

	ArrayList<Rule> ruleset = new ArrayList<Rule>();

	// Trains the classifier and builds the rule set
	public void buildClassifier(Instances trainingData) throws Exception {
		for (Instance instance : trainingData) {
			
		}	
	}

	public double classifyInstance(Instance instance) {
		return 0.5;
	}

	public String toString() {
		return "PRISM implemented by Clayton Johnson";
	}

}
