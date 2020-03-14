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

public class IB2 extends AbstractClassifier {
	protected int m_K = 1;
	protected NearestNeighbourSearch m_NNSearch = new LinearNNSearch();

	public void buildClassifier(Instances trainingData) throws Exception {
		trainingData = new Instances(trainingData);
		trainingData.deleteWithMissingClass();

		// For every training instance, we only remember it if we misclassify it
		m_NNSearch.setInstances(new Instances(trainingData, 1, 1));
		for (Instance train_x : trainingData) {
			Instances neighbours = m_NNSearch.kNearestNeighbours(train_x, m_K);

			// Classify the training instance
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

			System.out.println("Training instance: " + train_x.toString());
			System.out.println("Classes: " + train_x.classAttribute().toString());
			System.out.println("Classified as: " + train_x.classAttribute().value(max).toString());
			System.out.println("Class is: " + train_x.classAttribute().value((int)train_x.classValue()).toString());
			//System.out.println(train_x.classValue());
			//System.out.println(Arrays.toString(dist));

			if (train_x.classAttribute().value(max) != train_x.classAttribute().value( (int) train_x.classValue() )) {
				m_NNSearch.update(train_x);
				System.out.println("Incorrect!");
			} else {
				System.out.println("Correct!");
			}

			
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
