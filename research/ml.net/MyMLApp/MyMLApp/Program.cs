//using MyMLApp;

//// See https://aka.ms/new-console-template for more information
//Console.WriteLine("Hello, World!");
//// Add input data
//var sampleData = new MLModel1.ModelInput()
//{
//    Col0 = "This restaurant was wonderful."
//};

//// Load model and predict output of sample data
//var result = MLModel1.Predict(sampleData);

//// If Prediction is 1, sentiment is "Positive"; otherwise, sentiment is "Negative"
//var sentiment = result.PredictedLabel == 1 ? "Positive" : "Negative";
//Console.WriteLine($"Text: {sampleData.Col0}\nSentiment: {sentiment}");
using System;
using Microsoft.ML;
using Microsoft.ML.Data;
using System.Linq;
using System.IO.Compression;
using System.Net;
using MyMLApp;

public class SudoCommandData
{
    [LoadColumn(0)]
    public bool Label { get; set; }

    [LoadColumn(1)]
    public string Command { get; set; }
}

public class CommandPrediction
{
    [ColumnName("PredictedLabel")]
    public bool IsSafe { get; set; }

    public float[] Score { get; set; }
}

//class Program
//{
//    static void Main(string[] args)
//    {
//        // 1. Créer le contexte ML
//        var mlContext = new MLContext();

//        // 2. Charger les données CSV
//        string dataPath = "C:\\devel\\searchbot\\research\\ml.net\\MyMLApp\\MyMLApp\\dangerous_sudo_commands_fixed.csv"; // Assure-toi que le chemin est correct.
//        IDataView dataView = mlContext.Data.LoadFromTextFile<SudoCommandData>(
//            dataPath,
//            separatorChar: ',',
//            hasHeader: true
//        );

//        // 3. Diviser les données en ensemble d'entraînement et de test
//        var splitData = mlContext.Data.TrainTestSplit(dataView, testFraction: 0.2);
//        var trainingData = splitData.TrainSet;
//        var testData = splitData.TestSet;

//        // 4. Construire le pipeline de transformation et d'entraînement
//        var pipeline = mlContext.Transforms.Text.FeaturizeText("Features", nameof(SudoCommandData.Command)) // TF-IDF vectorizer
//            .Append(mlContext.Transforms.Concatenate("Features", "Features"))
//            .Append(mlContext.BinaryClassification.Trainers.FastTree(labelColumnName: "Label", featureColumnName: "Features"));

//        // 5. Entraîner le modèle
//        var model = pipeline.Fit(trainingData);

//        // 6. Évaluer le modèle
//        var predictions = model.Transform(testData);
//        var metrics = mlContext.BinaryClassification.Evaluate(predictions, "Label");

//        // 7. Afficher les résultats d'évaluation
//        Console.WriteLine($"Accuracy: {metrics.Accuracy:P2}");
//        Console.WriteLine($"AUC: {metrics.AreaUnderRocCurve:P2}");
//        Console.WriteLine($"F1 Score: {metrics.F1Score:P2}");

//        // 8. Effectuer des prédictions sur de nouvelles commandes
//        var predictionEngine = mlContext.Model.CreatePredictionEngine<SudoCommandData, CommandPrediction>(model);

//        var newCommand = new SudoCommandData { Command = "sudo systemctl restart nginx" };
//        var prediction = predictionEngine.Predict(newCommand);

//        Console.WriteLine($"Commande: {newCommand.Command}");
//        Console.WriteLine($"Prédiction - Dangereux? {prediction.IsDangerous}, Score: {prediction.Score}");
//    }
//}

class Program
{
    static void Main(string[] args)
    {
        //// Download the dataset if it doesn't exist.
        //if (!File.Exists(TrainDataPath))
        //{
        //    using (var client = new WebClient())
        //    {
        //        //The code below will download a dataset from a third-party, UCI (link), and may be governed by separate third-party terms. 
        //        //By proceeding, you agree to those separate terms.
        //        client.DownloadFile("https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip", "spam.zip");
        //    }

        //    ZipFile.ExtractToDirectory("spam.zip", DataDirectoryPath);
        //}

        // Set up the MLContext, which is a catalog of components in ML.NET.
        MLContext mlContext = new MLContext();

        // Specify the schema for spam data and read it into DataView.
        var path = "C:\\devel\\searchbot\\research\\ml.net\\MyMLApp\\MyMLApp\\dangerous_sudo_commands_fixed.csv";
        var data = mlContext.Data.LoadFromTextFile<SudoCommandData>(path: path, hasHeader: true, separatorChar: ',');

        // Create the estimator which converts the text label to boolean, featurizes the text, and adds a linear trainer.
        // Data process configuration with pipeline data transformations 
        var dataProcessPipeline = mlContext.Transforms.Conversion.MapValueToKey("Label", "Label")
                                  .Append(mlContext.Transforms.Text.FeaturizeText("commandText", new Microsoft.ML.Transforms.Text.TextFeaturizingEstimator.Options
                                  {
                                      WordFeatureExtractor = new Microsoft.ML.Transforms.Text.WordBagEstimator.Options { NgramLength = 2, UseAllLengths = true },
                                      CharFeatureExtractor = new Microsoft.ML.Transforms.Text.WordBagEstimator.Options { NgramLength = 3, UseAllLengths = false },
                                      Norm = Microsoft.ML.Transforms.Text.TextFeaturizingEstimator.NormFunction.L2,
                                  }, "Command"))
                                  .Append(mlContext.Transforms.CopyColumns("command", "commandText"))
                                  .AppendCacheCheckpoint(mlContext);


        // Set the training algorithm 
        var trainer = mlContext.MulticlassClassification.Trainers.OneVersusAll(mlContext.BinaryClassification.Trainers.AveragedPerceptron(labelColumnName: "Label", numberOfIterations: 10, featureColumnName: "command"), labelColumnName: "Label")
                                  .Append(mlContext.Transforms.Conversion.MapKeyToValue("PredictedLabel", "PredictedLabel"));
        var trainingPipeLine = dataProcessPipeline.Append(trainer);

        // Evaluate the model using cross-validation.
        // Cross-validation splits our dataset into 'folds', trains a model on some folds and 
        // evaluates it on the remaining fold. We are using 5 folds so we get back 5 sets of scores.
        // Let's compute the average AUC, which should be between 0.5 and 1 (higher is better).
        Console.WriteLine("=============== Cross-validating to get model's accuracy metrics ===============");
        var crossValidationResults = mlContext.MulticlassClassification.CrossValidate(data: data, estimator: trainingPipeLine, numberOfFolds: 5);
        ConsoleHelper.PrintMulticlassClassificationFoldsAverageMetrics(trainer.ToString(), crossValidationResults);

        // Now let's train a model on the full dataset to help us get better results
        var model = trainingPipeLine.Fit(data);

        //Create a PredictionFunction from our model 
        var predictor = mlContext.Model.CreatePredictionEngine<SudoCommandData, CommandPrediction>(model);

        Console.WriteLine("=============== Predictions for below data===============");
        // Test a few examples
        ClassifyMessage(predictor, "sudo /bin/sh");
        ClassifyMessage(predictor, "sudo systemctl restart nginx");
        ClassifyMessage(predictor, "sudo systemctl start httpd");
        ClassifyMessage(predictor, "sudo System.Diagnostics.Process.Start(\"\"/bin/vim\"\").WaitForExit();");


        // Lire chaque ligne du dataset et faire la prédiction
        var dataEnumerable = mlContext.Data.CreateEnumerable<SudoCommandData>(data, reuseRowObject: false);
        foreach (var commandData in dataEnumerable)
        {
            var prediction = predictor.Predict(commandData);

            if (commandData.Label != prediction.IsSafe)
            {
                // Afficher les résultats
                Console.WriteLine($"Commande: {commandData.Command}");
                Console.WriteLine($"Véritable label (safe?): {commandData.Label}");
                Console.WriteLine($"Prédiction - IsSafe? {prediction.IsSafe}, Score: {string.Join(",", prediction.Score)}");
                Console.WriteLine(new string('-', 50));
            }

        }

            Console.WriteLine("=============== End of process, hit any key to finish =============== ");
        Console.ReadLine();
    }

    public static void ClassifyMessage(PredictionEngine<SudoCommandData, CommandPrediction> predictor, string message)
    {
        var input = new SudoCommandData { Command = message };
        var prediction = predictor.Predict(input);

        Console.WriteLine("The message '{0}' is {1}", input.Command, prediction.IsSafe ? "safe" : "dangerous");
    }
}

