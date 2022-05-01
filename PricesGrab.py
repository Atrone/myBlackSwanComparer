from MyBlackSwanDB import MyBlackSwanDB
#from coinmarketcapapi import CoinMarketCapAPI
import time
from pycoingecko import CoinGeckoAPI
from pycoinmarketcap import CoinMarketCap

class PricesGrab:
    def __init__(self, mbsDB : MyBlackSwanDB = MyBlackSwanDB()):
        self.aggResultsPriceSaved = mbsDB.aggResultsSaved[0]
        self.cg = CoinGeckoAPI()
        self.cmc = CoinMarketCap('')
        self.coin_list = (self.cg.get_coins_list())

    def getPriceForCryptoAtTimeDB(self,crypto, date):
        for price in self.aggResultsPriceSaved:
            if str(price['start']).split(" ")[0] == str(date).split(" ")[0]:
                if crypto + " crypto" in price['price'].keys():
                    return price['price'][crypto + " crypto"]
                else:
                    return None
        return None

    def getPriceForCryptoAtTimeCMC(self,crypto, date):
        time.sleep(2)
        price = self.cmc.tools_price_conversion(amount=1, symbol=crypto, time=date)
        if 'quote' in price.data:
            return price.data['quote']['USD']['price']
        else:
            return None

    def getPriceForCryptoAtTimeCoinGecko(self,crypto, date):
        time.sleep(3)
        if crypto == "BTT":
            return None
        if ('market_data' in self.cg.get_coin_history_by_id(
                next(item for item in self.coin_list if item["symbol"] == (crypto.lower()))['id'],
                date.strftime("%d-%m-%Y")).keys()):
            return float(
                self.cg.get_coin_history_by_id(next(item for item in self.coin_list if item["symbol"] == (crypto.lower()))['id'],
                                          date.strftime("%d-%m-%Y"))['market_data']["current_price"]["usd"])
        else:
            return None
