# metadata-dashboard 

##Executive Summary

Most business decisions are not split test and it is difficult to determine the impact of an intervention. Our dashboard provides an analyst the ability to add context to their time series data and help infer the impact of a given intervention.

Source (of inspiration):
http://blog.iron.io/2014/10/how-to-build-etl-pipeline-for.html

##Data Generation:

There are three Input datasets coming through our data pipelines:

- Business event data coming from segment, including CRM and Web Analytics data
- High dimensional metadata that includes information about the state of the world
- Intervention data that includes business events of interest

The simulations that generate the data and load it into the pipelines can be found in the data-generation folder

##ETL processes

Once the data has entered the pipeline, it is queued iron.io until a worker is ready to process the event.The python scripts in the worker folder index the data into Elastic Search, where it is available for analysis. 

## Insight generation

The three types of data are fed into insight generation engine, which attempts to infer the causal impact of each intervention. The model being used ... TBD and the output of this model helps an analyst understand which interventions were most successful.

## Presentation and Visualization

We used Kibana for visualization and data exploration of the data in Elasticsearch, which allows an analyst to plot trends and generate additional aggregations to understand what contributed to the relative success of interventions.

Built by: Geoff, Adam, Matt and Athens
