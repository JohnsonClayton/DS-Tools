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
import java.util.List;
import java.util.Collections;
import java.util.Comparator;

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
			//System.out.println("--------- New Instance ----------");
			boolean ret = false;
			Attribute attr;
			String val;
			for (int i = 0; i < instance.numAttributes() && i != instance.classIndex(); i++) {
				attr = instance.attribute(i);
				val = instance.stringValue(attr);

				if (this.attribute == i && this.value == val) {
					ret = true;
				}

				//System.out.println("======================");
				//System.out.println(i + " matches to " + this.attribute);
				//System.out.println(val + " matches to " + this.value + " : " + ret);
			}
			return ret;
		}

		public boolean equals(Rule rule) {
			boolean ret = false;
			if (rule.getAttribute() == this.attribute && rule.getValue() == this.value && rule.getClassification() == this.classification)
				ret = true;
			return ret;
		}

		//@Override
		//public int compareTo(Rule rule) {
		//	return Integer.compare(this.matches, rule.getSuccesses());
		//}

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

		public void setRules(List<Rule> _rules) {
			this.rules = (ArrayList<Rule>)_rules;
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

		public void remove(Rule rule) {
			this.rules.remove(rule);
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

	private class DerivedRule {
		private ArrayList<Integer> attributes = new ArrayList<Integer>();
		private ArrayList<String> values = new ArrayList<String>();
		private String classification = null;

		public DerivedRule(Rule rule) {
			if (rule != null) {
				this.attributes.add(rule.getAttribute());
				this.values.add(rule.getValue());
				this.classification = rule.getClassification();
			}
		}

		public DerivedRule(Rules ruless) {
			if (ruless != null) {
				ArrayList<Rule> reglas = ruless.getRules();
				for (int i=0; i < reglas.size(); i++) {
					this.attributes.add(reglas.get(i).getAttribute());
					this.values.add(reglas.get(i).getValue());
					this.classification = reglas.get(i).getClassification();
				}
			}
		}

		public DerivedRule(ArrayList<Rule> ruless) {
			if (ruless != null) {
				for (int i=0; i < ruless.size(); i++) {
					this.attributes.add(ruless.get(i).getAttribute());
					this.values.add(ruless.get(i).getValue());
					this.classification = ruless.get(i).getClassification();
				}
			}
		}

		public boolean instanceMatches(Instance instance) {
			//System.out.println("--------- New Instance ----------");
			boolean ret = true;
			Attribute attr;
			String val;
			for (int i = 0; i < instance.numAttributes() && i != instance.classIndex(); i++) {
				attr = instance.attribute(i);
				val = instance.stringValue(attr);
				for (int j = 0; j < this.attributes.size(); j++) {
					if (this.attributes.get(j) != i || this.values.get(j) != val) {
						ret = false;
					}
				}

				//System.out.println("======================");
				//System.out.println(i + " matches to " + this.attribute);
				//System.out.println(val + " matches to " + this.value + " : " + ret);
			}
			return ret;
		}

		public String getClassification() {
			return this.classification;
		}

		public String toString() {
			String output = "IF ";
			output += this.attributes.get(0) + " = " + this.values.get(0) + ",\n";
			for (int i=1; i<this.attributes.size()-1 ; i++) {
				output += "   and " + this.attributes.get(i) + " = " + this.values.get(i) + ",\n";
			}
			output += "   and " + this.attributes.get(this.attributes.size()-1) + " = " + this.values.get(this.attributes.size()-1) + " : " + this.classification + "\n";
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
	private ArrayList<DerivedRule> derived_rules = new ArrayList<DerivedRule>();
	private ArrayList<Rule> rules_accumulated = new ArrayList<Rule>();

	private void filterOff(Attribute class_attr, int class_number, Instances instances) {
		// If there is only one class in instances, then we should return
		Attribute class_at;
		String classification;
		ArrayList<String> classifications = new ArrayList<String>();
		for (Instance instance : instances) {
			classification = instance.classAttribute().value( (int) instance.classValue() );
			if (!classifications.contains(classification)) {
				classifications.add(classification);
			}
		}
		//System.out.println("Printing classifications...");
		//System.out.println(classifications);
		//System.out.println("...End classifications");
		if (classifications.size() == 1) {
			derived_rules.add(new DerivedRule(rules_accumulated));
			return;
		}
		


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
					//System.out.println(instances.get(j));
				} else {
					subset.add(instances.get(j));
				}
			}
		}
		rules_accumulated.add(rule);
		rules.remove(rule);
		if (subset != null) {
			//System.out.println("Size of subset is: " + subset.numInstances() + " out of " + instances.numInstances());
			filterOff(class_attr, class_number, subset);
			derived_rules.add(new DerivedRule(rules_accumulated));
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
		//System.out.println(class_attr);
		int class_count = class_attr.numValues();
		for (int i=0; i<class_count; i++) {

			filterOff(class_attr, i, trainingData);
		}	
		Collections.sort(this.rules.getRules(), new Comparator<Rule>() {
			public int compare(Rule rule1, Rule rule2) {
				return Integer.compare(rule2.getSuccesses(), rule1.getSuccesses());
			}
		});
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
		if(derived_rules.isEmpty()) {
			return 0.0;
		} else {
			DerivedRule rule = derived_rules.get(0);
			for (DerivedRule rule1 : derived_rules) {
				if (rule1.instanceMatches(instance)) {
					rule = rule1;
				}
			}
			return 1.0*instance.classAttribute().indexOfValue(rule.getClassification());
		}
	}

	// This will automatically be called and output the ruleset
	public String toString() {
		String output = "PRISM implemented by Clayton Johnson\n";
		for (DerivedRule rule : derived_rules) output += rule.toString();
		//output += derived_rules.toString();
		return output;
	}

}
