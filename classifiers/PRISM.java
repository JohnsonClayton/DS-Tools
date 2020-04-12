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

	private class Rules {
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

	// Trains the classifier and builds the rule set
	public void buildClassifier(Instances trainingData) throws Exception {

		for (Instance instance : trainingData) {
			// Add all of the rules to the rule set
			rules.addRules( createRulesFromInstance(instance) );
		}
		
		//for (Instance instance : trainingData) {
			// Calculate the probability of occurrence p(o_n | a_x) of the classification o_n for each attribute-value pair a_x

			// 	Find the rule with the highest probability
			

			// Select the a_x for which p(o_n | a_x) is a maximum and create a subset of the training set comprising all the instances which contain the selected a_x
			// Repeat steps 1-2 for this subset until it contains only instances of class o_n. The induced rule is a conjunction of all the attribute-value pairs used in creating the homogeneous subset.
			// Remove all instances covered by this rule from the training set.
			// Repeat steps 1-4 until all instances of class o_n have been removed
		//}	

	}

	public double classifyInstance(Instance instance) {
		return 0.5;
	}

	public String toString() {
		String output = "PRISM implemented by Clayton Johnson\n";
		output += rules.toString();
		return output;
	}

}
