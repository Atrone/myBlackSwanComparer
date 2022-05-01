from datetime import datetime

from mymongo import MyMongo

queryTrendAndPrevTrend = [
    {
        "$match": {
            "start": {
                "$gte": datetime.strptime("2021-08-02T00:15:31", "%Y-%m-%dT%H:%M:%S")
            }
        }
    },
    {
        "$sort": {
            "_id": 1.0
        }
    },
    {
        "$match": {
            "trends": {
                "$ne": None
            }
        }
    },
    {
        "$group": {
            "_id": 0.0,
            "document": {
                "$push": "$$ROOT"
            }
        }
    },
    {
        "$project": {
            "documentAndPrevTrends": {
                "$zip": {
                    "inputs": [
                        "$document",
                        {
                            "$concatArrays": [
                                [
                                    None
                                ],
                                "$document.trends"
                            ]
                        }
                    ]
                }
            }
        }
    },
    {
        "$unwind": {
            "path": "$documentAndPrevTrends"
        }
    },
    {
        "$replaceRoot": {
            "newRoot": {
                "$mergeObjects": [
                    {
                        "$arrayElemAt": [
                            "$documentAndPrevTrends",
                            0.0
                        ]
                    },
                    {
                        "prevTrends": {
                            "$arrayElemAt": [
                                "$documentAndPrevTrends",
                                1.0
                            ]
                        }
                    }
                ]
            }
        }
    }
]

queryPrices = [
    {
        "$match": {
            "start": {
                "$gte": datetime.strptime("2021-08-02T00:15:31", "%Y-%m-%dT%H:%M:%S")
            }
        }
    },
    {
        "$sort": {
            "_id": 1.0
        }
    },
    {
        "$match": {
            "price": {
                "$ne": None
            }
        }
    }
]


class MyBlackSwanDB:
    def __init__(self, queries=None,
                 mongo_conn: MyMongo = MyMongo(""
                                               ),
                 db="example_db", col="test_collection"):
        self.aggResults = []
        self.mongo_conn = mongo_conn
        self.db = db
        self.col = col
        if queries is None:  # default
            queries = [queryTrendAndPrevTrend, queryPrices]
            for query in queries:
                self.aggResults.append(self.mongo_conn.run_aggregation(self.db, self.col, query))
            self.trendDiffs = []
            self.prices = []
            self.aggResultsSaved = []

            self.saveAggResult(1)

            for agg_result_trendAndPrevTrend, agg_result_price_saved in (
                    zip(self.aggResults[0], self.aggResultsSaved[0])):
                self.trendDiffs, self.prices = self.buildMyBlackSwanDBDefaultDictionary(agg_result_trendAndPrevTrend,
                                                                                        agg_result_price_saved)
        else:
            print("Not default params, do yer own damn insights!")

    def saveAggResult(self, i):
        self.aggResultsSaved.append([])
        for a in self.aggResults[i]:
            self.aggResultsSaved[len(self.aggResultsSaved) - 1].append(a)

    def buildMyBlackSwanDBDefaultDictionary(self, agg_result_trendAndPrevTrend, agg_result_price_saved):
        self.trendDiffs.append({})
        self.prices.append({})
        for k in agg_result_trendAndPrevTrend['trends'].keys():
            if agg_result_trendAndPrevTrend['prevTrends']:
                for k2 in agg_result_trendAndPrevTrend['prevTrends'].keys():
                    if k == k2:
                        self.trendDiffs[len(self.trendDiffs) - 1][
                            k + "_" + str(agg_result_trendAndPrevTrend['start'])] = float(
                            agg_result_trendAndPrevTrend['trends'][k]) - float(
                            agg_result_trendAndPrevTrend['prevTrends'][k2])
                        self.prices[len(self.prices) - 1][k + "_" + str(agg_result_trendAndPrevTrend['start'])] = float(
                            agg_result_price_saved['price'][k])
        return self.trendDiffs, self.prices
