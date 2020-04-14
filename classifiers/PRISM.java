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

	private class Rule implements Serializable {
		// Actions depend on the data type of the given relationship
		private int attribute = 0;
		private String value = null;
		private String classification = null;
		private int matches = 1;

		public Rule(int attr, String val, String classif) {
			this.attribute = attr;
			this.value = val;
			this.classification = classif;  
		}

		public void addOne() {
			this.matches++;
		}

		public int getAttribute() {
			return this.attribute;
		}

		public String getValue() {
			return this.value;
		}

		public String getClassification() {
			return this.classification;
		}

		public int getSuccesses() {
			return this.matches;
		}

		public boolean instanceMatches(Instance instance) {
			boolean ret = false;
			Attribute attr;
			String val;
			for (int i = 0; i < instance.numAttributes(); i++) {
				attr = instance.attribute(i);
				val = instance.stringValue(attr);

				if (this.attribute == i && this.value == val) {
					ret = true;
				}
			}
			return ret;
		}

		public boolean equals(Rule rule) {
			boolean ret = false;
			if (rule.getAttribute() == this.attribute && rule.getValue() == this.value && rule.getClassification() == this.classification)
				ret = true;
			return ret;
		}

		public String toString() {
			String output = this.attribute + "\t=>\t" + this.value + "\t|\t" + this.classification + "(" + this.matches + ")";
			return output;
		}
	}

	private class Rules implements Serializable {
		private ArrayList<Rule> rules;

		public Rules() {
			this.rules = new ArrayList<Rule>();
		}

		public Rules(Rule rule) {
			this.rules = new ArrayList<Rule>();
			this.rules.add(rule);
		}

		public int containsRule(Rule rule) {
			int index = -1;

			for (int i = 0; i < this.rules.size(); i++) {
				if ( (this.rules.get(i)).equals(rule) ) index = i;
			}

			return index;
		}

		public void addRule(Rule rule) {
			int index = containsRule(rule);
			if (index < 0 ) {
				// Add the rule to the list if it doesn't exist
				this.rules.add(rule);
			} else {
				// If the rule already exists, add one to its successes
				this.rules.get( index ).addOne();
			}	
		}

		public void addRules(Rules rules) {
			for (Rule rule : rules.getRules()) 
				addRule(rule);
		}

		public ArrayList<Rule> getRules() {
			return this.rules;
		}

		public boolean isEmpty() {
			return this.rules.size() == 0;
		}

		public String toString() {
			String output = "Attribute\t=>\tValue \t|\tClassification";
			for (Rule rule : getRules()) {
				output += "\n";
				output += rule.toString();
			}
			return output;
		}

	}

	private Rules createRulesFromInstance(Instance instance) {

		Rules rules = new Rules();		

		// The instance is classified to this classification
		String classification = instance.classAttribute().value( (int) instance.classValue() );
		for (int i = 0; i < instance.numAttributes() && i != instance.classIndex(); i++) {

			// Acquire the attribute name and value
			Attribute attribute = instance.attribute(i);
			String value = instance.stringValue(attribute);

			// Create and add the rule to the ruleset
			Rule rule = new Rule(i, value, classification);
			rules.addRule(rule);
		}
		return rules;
	}

	private Rules rules = new Rules();

	private void filterOff(Attribute class_attr, int class_number, Instances instances) {
		// Select the a_x for which p(o_n | a_x) is a maximum and create a subset of the training set comprising all the instances which contain the selected a_x
		// 	Find the rule with the highest probability
		Rule rule = null;
		for (Rule rule1 : this.rules.getRules()) {
			if ( (int) (class_attr.indexOfValue(rule1.getClassification())) == class_number && (rule == null ||  rule1.getSuccesses() > rule.getSuccesses()) ) {
				rule = rule1;
			}
		}

		//System.out.println("Highest for classification " + i + " is: " + rule.toString());

		//	Create a subset of the training set comprising all the instances which contain the selected a_x
		Instances subset = null;
		for (int j=0; j<instances.numInstances(); j++) {
			// If the instance matches with the rule, then add it to the subset
			if (rule.instanceMatches(instances.get(j))) {
				if (subset == null) {
					subset = new Instances(instances, j, 1);
				} else {
					subset.add(instances.get(j));
				}
			}
		}
		if (subset != null) {
			System.out.println("Size of subset is: " + subset.numInstances() + " out of " + instances.numInstances());
		} else {
			System.out.println("The subset was never made...");
		}
	}

	// Trains the classifier and builds the rule set
	public void buildClassifier(Instances trainingData) throws Exception {

		// Calculate the probability of occurrence p(o_n | a_x) of the classification o_n for each attribute-value pair a_x
		for (Instance instance : trainingData) {
			// Add all of the rules to the rule set
			rules.addRules( createRulesFromInstance(instance) );
		}
		
		// For each classification	
		Instance instance = trainingData.firstInstance();
		Attribute class_attr = instance.classAttribute();
		System.out.println(class_attr);
		int class_count = class_attr.numValues();
		for (int i=0; i<class_count; i++) {

			filterOff(class_attr, i, trainingData);
			// Repeat steps 1-2 for this subset until it contains only instances of class o_n. The induced rule is a conjunction of all the attribute-value pairs used in creating the homogeneous subset.
			// Remove all instances covered by this rule from the training set.
			// Repeat steps 1-4 until all instances of class o_n have been removed
		}	

	}

	public double classifyInstance(Instance instance) {
		//String attr1 = "no-recurrence-events";
		//String attr2 = "recurrence-events";
		//System.out.println(instance.classAttribute().indexOfValue(attr1));
		//System.out.println(instance.classAttribute().indexOfValue(attr2));
		/*double ret = -1.0;
		for (Rule rule : this.rules.getRules()) {
			if (rule.instanceMatches(instance)) {
				ret = 1.0*instance.classAttribute().indexOfValue(rule.getClassification());
			}
		}*/
		Rule rule = null;
		for (Rule rule1 : this.rules.getRules()) {
			if ( (rule1.instanceMatches(instance)) && (rule == null ||  rule1.getSuccesses() > rule.getSuccesses()) ) {
				rule = rule1;
			}
		}
		return 1.0*instance.classAttribute().indexOfValue(rule.getClassification());
	}

	public String toString() {
		String output = "PRISM implemented by Clayton Johnson\n";
		output += rules.toString();
		return output;
	}

}
