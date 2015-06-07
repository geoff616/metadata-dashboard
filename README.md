# metadata-dashboard 

##Executive Summary

We want to able to demonstrate to conduct ETL processes across:
  Extract: Segment.io
  Transform: Ironworker
  Load: ElasticSearh
To continuously generate insights for a ski resort manager.

In the older workflow, this manager would have to manually ETL in batch, and run that through his data modelling in batch.  With this new workflow, we hope to be able to run ETL, data modelling (and recommendations!) continuously.

Source (of inspiration):
http://blog.iron.io/2014/10/how-to-build-etl-pipeline-for.html

##Data Generation:

There are three Input datasets coming from Segment:
Unaggregated Event Data - this consititues 
High Dimension Metadata
Intervention Data
These are all found in the data-generation folder

##ETL processes

The scripts used to ETL  are found in the workers folder.  The python scripts here takes the data generated and ETL them into Elastic Search, through using workers from Iron.io.  To learn more about Iron and workers, see http://dev.iron.io/worker/beta/getting_started/ for more details

## Insight generation

We feed the loaded data into insight generation engine which provides metrics such as Revenue Lift ($)

UPDATE: We would have ideally wanted to separate i) ETL and ii) Insights Generation as separate steps into and out of Elastic Search, i.e. Load into Elastic Search, pull data from Elastic Search and feed into Insights Generation, and Load results back into Elastic Search.  However, due to insufficient time, we merged the two steps into one.

## Presentation and Visualization

We used Kibana for visualization (and seredipidous insight generation :) ) which nicely talks to Elastic Search.

Geoff, Adam, Matt and Athens



