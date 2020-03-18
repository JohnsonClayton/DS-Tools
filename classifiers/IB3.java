/*  Instance-based Classifier 2 implemented by Clayton Johnson
 *    as described in Aha's Paper: Instance-Based Learning Algorithm
 *
 *
 *   IB-2:
 *   ------------------------
 *   CD = null
 *   for each x in x_train do
 *   1. for each y in CD do
 *     Sim[y] <- Similarity(x, y)
 *   2. y_max <- some y in CD with maximal Sim[y]
 *   3. if class(x) == class(y_max)
 *      then classification <- correct
 *      else
 *        classification <- incorrect
 *        CD <- CD unioned {x}
 *
 *    
 *
 */

package weka.classifiers.lazy;

import java.util.Collections;
import java.util.Enumeration;
import java.util.Vector;
import java.util.Arrays;
import java.util.HashMap;

import java.io.*;

import weka.classifiers.AbstractClassifier;
import weka.classifiers.UpdateableClassifier;
import weka.classifiers.rules.ZeroR;
import weka.core.AdditionalMeasureProducer;
import weka.core.Attribute;
import weka.core.Capabilities;
import weka.core.Capabilities.Capability;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.Option;
import weka.core.OptionHandler;
import weka.core.RevisionUtils;
import weka.core.SelectedTag;
import weka.core.Tag;
import weka.core.TechnicalInformation;
import weka.core.TechnicalInformation.Field;
import weka.core.TechnicalInformation.Type;
import weka.core.TechnicalInformationHandler;
import weka.core.Utils;
import weka.core.WeightedInstancesHandler;
import weka.core.neighboursearch.LinearNNSearch;
import weka.core.neighboursearch.NearestNeighbourSearch;

public class IB3 extends AbstractClassifier {
	protected int m_K = 1;
	protected NearestNeighbourSearch m_NNSearch = new LinearNNSearch();
	protected HashMap<Object, int[]> neighbourStats = new HashMap<Object, int[]>(); // Instance -> { complete classifications, total since added, total with same class }
	protected Instances conceptDescription; 

	// This will update the statistics of the given instance and classifications
	private void updateStatistics(Instance x, String pred_class, String real_class) {
		
	}

	private Instance randomInstance(Instances x) {
		// Return a random instance
		return x.get( (int) Math.random()*x.numInstances() );
	}

	// This will initialize the concept description with the first element in the training data set
	private void initCD(Instances train) throws Exception {
		// Take the first element in the training data and add it to the conceptDescription list
		conceptDescription = new Instances(train, 1, 1);

		// Add the same instance to the statistics for CD
		int[] arr = {0, 0};
		String key = conceptDescription.firstInstance().toStringNoWeight().replaceAll(",", "|");
		neighbourStats.put(key, arr); //conceptDescription.firstInstance(), arr);

		//System.out.println("I've just added the first key, " + key + ", to the HashMap!");
	}

	// This will add an instance to the concept description and the HashMap to keep track of statistics
	private void addInstancetoCD(Instance x) throws Exception {
		if (conceptDescription != null) {
			conceptDescription.add(x);
			m_NNSearch.setInstances(conceptDescription);

			// Statistics
			int[] arr = {0, 0};
			String key = x.toStringNoWeight().replaceAll(",", "|");
			neighbourStats.put(key, arr);
			//System.out.println("I've just added " + key + " to the HashMap!");
		} else {
			System.err.println("conceptDescription is null!");
		}
	}


	/* This function will return the neighbours that have good track records so far (90%) accuracy
 	 *   The heuristics used are presented in Reduction Techniques for Instance-Based Learning Algorithms by Wilson-Martinez (2000)
	 *   Formula for the upper and lower bounds of the conf. interval is:
	 *
	 *   p + (z^2 / 2n) +- z*sqrt(q)
	 *   --------------------------  , where q = ( p*(1-p)/n ) + (z^2 / 4*n^2) )
	 *          1 + (z^2 / n)
	 *
	 *   Accuracy:
	 *     n is the number of classification attempts since introduction of instance to S (CD in Aha's work)
	 *     p is the accuracy of those attempts ( correct classification / n)
	 *
	 *   Frequency:
	 *     n is the number of previously processed instances
	 *     p is the frequency (proportion of instances so far that are the same class)
	 *
	 *   z is the confidence (0.9 for acceptance and 0.7 for dropping) in both cases
	 */

	private boolean isAcceptable(int n, int p) {
		double z = 0.9;

		// Calculate lower bound of acc

		// Calculate upper bound of freq			
		
			
		return true;
	}

	private boolean isPoor(int n, int p) {
		double z = 0.7;

		// Calculate upper bound of acc

		// Calculate lower bound of freq			

		return false;
	}

	private boolean hasPoorPerformance(Instance x) {
		boolean poor = false;
		String key = x.toStringNoWeight().replaceAll(",", "|");
		if (neighbourStats.containsKey(key)) {
			int[] stats = neighbourStats.get(key);
			if (isPoor(stats[0], stats[1])) {
				poor = true;
			}
		}
		return poor;
	}

	private Instances getAcceptableNeighbours(Instance x) throws Exception {

		Instances neighbours = m_NNSearch.kNearestNeighbours(x, m_K);

		double z, p;
		int[] stats = new int[2];
		Instance neighbour;

		for (int i = 0; i < neighbours.size(); i++) {
			neighbour = neighbours.get(i);
			String key = neighbour.toStringNoWeight().replaceAll(",", "|");
			if (neighbourStats.containsKey(key)) {
				// Remove the neighbour instances that do not meet the specifications:
				//   Lower bound of acc is higher than the upper bound of the frequency of its class
				stats = neighbourStats.get(key);
				if (!isAcceptable(stats[0], stats[1])) {
					neighbours.remove(i);
				}

			}
		}
		return neighbours;
	}

	// This method will create + train the classifier
	public void buildClassifier(Instances trainingData) throws Exception {
		trainingData = new Instances(trainingData);
		trainingData.deleteWithMissingClass();

		int[] stats = new int[3];

		// Initialize the search spaces and concept description
		m_NNSearch.setInstances(new Instances(trainingData, 1, 1));
		initCD(trainingData);

		// Start the training...
		for (Instance train_x : trainingData) {
			// Only take the neighbours will acceptable statistics
			Instances neighbours = getAcceptableNeighbours(train_x);
			if (neighbours.numInstances() == 0) {
				neighbours.add(randomInstance(conceptDescription));
			}

			// Classify the training instance <- This would be better to create and implement the classify function here
			double[] dist = new double[train_x.numClasses()];
			for (Instance neighbour : neighbours) {
				if (train_x.classAttribute().isNominal()) {
					dist[(int)neighbour.classValue()] += 1.0 / neighbours.numInstances();
				} else {
					dist[0] += neighbour.classValue() / neighbours.numInstances();
				}
			}

			// This finds the index of the classification with the highest probability
			int max = 0;
			for (int i=0; i<dist.length-1; i++) {
                        	if (dist[max] < dist[i+1]) {
					max = i+1;
				}
			}

			// Finds the predicted classification (using the max from above) and the real classification
			String pred = train_x.classAttribute().value(max);
			String clss = train_x.classAttribute().value( (int) train_x.classValue() );

			if (clss != "" && pred != "" && clss != pred) {
				// The classification was incorrect
				//conceptDescription.add(train_x);
				addInstancetoCD(train_x);
			}

			// For every y in the CD
			for (Instance y : conceptDescription) {
				for (Instance neighbour : neighbours) {
					// If y is in neighbours
					if ( y.toStringNoWeight() == neighbour.toStringNoWeight() ) {
						// Update y's statistics
						updateStatistics(y, pred, clss);
					}

				}


				// If y's stats are bad enough, remove from CD
			}
			// Go through the entire CD and remove all the instances with poor performance
			for (int i=0; i < conceptDescription.size(); i++) {
				// If y has performed poorly
				if ( hasPoorPerformance( conceptDescription.get(i) ) ) {
					// Remove from CD
					conceptDescription.remove(i);
				}
			}

			m_NNSearch.setInstances(conceptDescription);
		}
	}

	public double[] distributionForInstance(Instance testInstance) throws Exception {
		m_NNSearch.addInstanceInfo(testInstance);

		Instances neighbours = m_NNSearch.kNearestNeighbours(testInstance, m_K);

		double[] dist = new double[testInstance.numClasses()];
		for (Instance neighbour : neighbours) {
			if (testInstance.classAttribute().isNominal()) {
				dist[(int)neighbour.classValue()] += 1.0 / neighbours.numInstances();
			} else {
				dist[0] += neighbour.classValue() / neighbours.numInstances();
			}
		}
		return dist;
	}
}
