from MyBlackSwanDB import MyBlackSwanDB
from PricesGrab import PricesGrab
from datetime import datetime


# 100 into SUPREME BUY MYBLACKSWAN EVERYDAY VS BITCOIN

# 50 into TOP 2 BUYS MYBLACKSWAN EVERYDAY VS BITCOIN

class MyBlackSwanCompare:
    def __init__(self, crypto: str, dollarsPerDay: int,
                 x: int,
                 pricesGrabber: PricesGrab = PricesGrab(),
                 mbsDB: MyBlackSwanDB = MyBlackSwanDB()):
        self.crypto = crypto
        self.x = x
        self.mbsDB = mbsDB
        self.dollarsPerDay = dollarsPerDay / self.x
        self.pricesGrabber = pricesGrabber
        self.portfolio = self.buildPortfolioMBSMaster()

    def buildRevenueCompare(self, portfolioCompare):
        revenueCompare = {}
        for p in portfolioCompare:
            revenueCompareDollars = 0
            for x in portfolioCompare[:portfolioCompare.index(p) + 1]:
                print(datetime.strptime(x.split("_")[1].split(" ")[0], "%Y-%m-%d"))
                price = (self.pricesGrabber.getPriceForCryptoAtTimeDB(self.crypto,
                                                                      datetime.strptime(p.split("_")[1].split(" ")[0],
                                                                                        "%Y-%m-%d")))
                if price is None:
                    revenueCompareDollars += float(x.split("_")[0]) * float(
                        (self.pricesGrabber.getPriceForCryptoAtTimeCoinGecko(self.crypto,
                                                                             datetime.strptime(
                                                                                 p.split("_")[1].split(" ")[0],
                                                                                 "%Y-%m-%d")))
                    )
                else:
                    revenueCompareDollars += float(x.split("_")[0]) * float(price
                                                                            )
                # time.sleep(5)
            revenueCompare[datetime.strptime(p.split("_")[1].split(" ")[0], "%Y-%m-%d")] = revenueCompareDollars
            print(revenueCompare)
        return revenueCompare

    def buildPortfolioCompare(self):
        portfolioCompare = []
        for p in self.portfolio:
            print(datetime.strptime(p.split("_")[2].split(" ")[0], "%Y-%m-%d"))
            price = (self.pricesGrabber.getPriceForCryptoAtTimeDB(self.crypto, datetime.strptime(
                p.split("_")[2].split(" ")[0], "%Y-%m-%d")))
            if price is None:
                price = (self.pricesGrabber.getPriceForCryptoAtTimeCoinGecko(self.crypto, datetime.strptime(
                    p.split("_")[2].split(" ")[0], "%Y-%m-%d")))
                portfolioCompare.append(str(self.dollarsPerDay / float(price)) + "_" + str(
                    datetime.strptime(p.split("_")[2].split(" ")[0], "%Y-%m-%d")))
            else:
                portfolioCompare.append(str(self.dollarsPerDay / float(price)) + "_" + str(
                    datetime.strptime(p.split("_")[2].split(" ")[0], "%Y-%m-%d")))
            print(portfolioCompare)
        return portfolioCompare

    def buildPortfolioMBSMaster(self):
        portfolio = []
        for trendDiff, price in zip(self.mbsDB.trendDiffs,
                                    self.mbsDB.prices):
            sortd = {k: v for k, v in sorted(trendDiff.items(), key=lambda item: item[1], reverse=True)}
            if sortd.keys():
                for buy in list(sortd.keys())[:self.x]:
                    portfolio.append(str(self.dollarsPerDay / price[buy]) + "_" + buy)
        print(portfolio)
        return portfolio

    def buildRevenueSwan(self):
        revenueSwan = {}
        for p in self.portfolio:
            revenueSwanDollars = 0
            for x in self.portfolio[:self.portfolio.index(p) + 1]:
                print(datetime.strptime(x.split("_")[2].split(" ")[0], "%Y-%m-%d"))
                price = (self.pricesGrabber.getPriceForCryptoAtTimeDB(x.split("_")[1].split(" ")[0],
                                                                      datetime.strptime(
                                                                          p.split("_")[2].split(" ")[0],
                                                                          "%Y-%m-%d")))
                if price is None:
                    price = (self.pricesGrabber.getPriceForCryptoAtTimeCoinGecko(x.split("_")[1].split(" ")[0],
                                                                                 datetime.strptime(
                                                                                     p.split("_")[2].split(" ")[
                                                                                         0],
                                                                                     "%Y-%m-%d")))
                    if price is None:
                        revenueSwanDollars += self.dollarsPerDay * 1.5
                    else:
                        revenueSwanDollars += float(x.split("_")[0]) * float(price)
                else:
                    revenueSwanDollars += float(x.split("_")[0]) * float(price)
            revenueSwan[datetime.strptime(p.split("_")[2].split(" ")[0], "%Y-%m-%d")] = revenueSwanDollars
            print(revenueSwan)
        return revenueSwan
