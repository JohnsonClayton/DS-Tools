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
	protected Instances dynamicTrainingInstances; 

	private void initCD(Instances train) throws Exception {
		// Take the first element in the training data and add it to the dynamicTrainingInstances list
		dynamicTrainingInstances = new Instances(train, 1, 1);

		// Add the same instance to the statistics for CD
		int[] arr = {0, 0, 0};
		String key = dynamicTrainingInstances.firstInstance().toStringNoWeight().replaceAll(",", "|");
		neighbourStats.put(key, arr); //dynamicTrainingInstances.firstInstance(), arr);

		System.out.println("I've just added the first key, " + key + ", to the HashMap!");
	}

	private void addInstancetoCD(Instance x) throws Exception {
		// Add this element to the NNSearch object and create a way to keep track of it's stats during training
		if (dynamicTrainingInstances != null) {
			dynamicTrainingInstances.add(x);
			m_NNSearch.setInstances(dynamicTrainingInstances);

			// Statistics
			int[] arr = {0, 0, 0};
			String key = x.toStringNoWeight().replaceAll(",", "|");
			neighbourStats.put(key, arr);
			System.out.println("I've just added " + key + " to the HashMap!");
		} else {
			System.err.println("dynamicTrainingInstances is null!");
		}
	}

	private Instances getAcceptableNeighbours(Instance x) throws Exception {
		// This function will return the neighbours that have good track records so far (90%) accuracy
		//   The heuristics used are presented in Reduction Techniques for Instance-Based Learning Algorithms by Wilson-Martinez (2000)
		//   Formula for the upper and lower bounds of the conf. interval is:
		//
		//   p + (z^2 / 2n) +- z*sqrt(q)
		//   --------------------------  , where q = ( p*(1-p)/n ) + (z^2 / 4*n^2) )
		//          1 + (z^2 / n)
		//
		//   Accuracy:
		//     n is the number of classification attempts since introduction of instance to S (CD in Aha's work)
		//     p is the accuracy of those attempts ( correct classification / n)
		//
		//   Frequency:
		//     n is the number of previously processed instances
		//     p is the frequency (proportion of instances so far that are the same class)
		//
		//   z is the confidence (0.9 for acceptance and 0.7 for dropping) in both cases

		Instances neighbours = m_NNSearch.kNearestNeighbours(x, m_K);

		double z, p;
		int[] stats;

		for (Instance neighbour : neighbours) {
			// Remove the neighbour instances that do not meet the specifications:
			//   Lower bound of acc is higher than the upper bound of the frequency of its class
			//stats = neighbourStats.get(neighbour);
			System.out.println(neighbourStats);
			System.out.println(neighbour);
			String key = neighbour.toStringNoWeight().replaceAll(",", "|");
			stats = neighbourStats.get(key);
			System.out.println(stats[0]);
			System.out.println(stats[1]);
			System.out.println(stats[2]);


			// Confidence for acceptance is 0.9
			z = 0.9;
			// Calculate lower bound of acc
			//   Calculate p
			//p = 

			// Calculate upper bound of freq			

			//System.out.println(stats);

		}

		return neighbours;
	}

	public void buildClassifier(Instances trainingData) throws Exception {
		trainingData = new Instances(trainingData);
		trainingData.deleteWithMissingClass();


		// For every training instance, we only remember it if we misclassify it
		//
		// We need to add this first instance to have at least one element in the search space
		m_NNSearch.setInstances(new Instances(trainingData, 1, 1));
		initCD(trainingData);
		for (Instance train_x : trainingData) {
			Instances neighbours = getAcceptableNeighbours(train_x); //m_NNSearch.kNearestNeighbours(train_x, m_K);

			// Classify the training instance <- This would be better to create and implement the classify function here
			double[] dist = new double[train_x.numClasses()];
			for (Instance neighbour : neighbours) {
				if (train_x.classAttribute().isNominal()) {
					dist[(int)neighbour.classValue()] += 1.0 / neighbours.numInstances();
				} else {
					dist[0] += neighbour.classValue() / neighbours.numInstances();
				}
			}

			// If classification is not correct, save the instance
			int max = 0;
			for (int i=0; i<dist.length-1; i++) {
                        	if (dist[max] < dist[i+1]) {
					max = i+1;
				}
			}

			//System.out.println("Training instance: " + train_x.toString());
			//System.out.println("Length of CD: " + m_NNSearch.getInstances().numInstances());
			//System.out.println("Options: " + train_x.classAttribute().toString());
			//System.out.println("Class is: " + train_x.classAttribute().value((int)train_x.classValue()).toString());
			//System.out.println("Classified as: " + train_x.classAttribute().value(max).toString());
			//System.out.println(train_x.classValue());
			//System.out.println(Arrays.toString(dist));

			String clss = train_x.classAttribute().value(max);
			String pred = train_x.classAttribute().value( (int) train_x.classValue() );

			if (clss != "" && pred != "" && clss != pred) {
				//m_NNSearch.update(train_x);
				dynamicTrainingInstances.add(train_x);
				/*System.out.println("Incorrect!");
			} else {
				System.out.println("Correct!");*/
			}

			m_NNSearch.setInstances(dynamicTrainingInstances);

			
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
