from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.technical import ma
from pyalgotrade.tools import yahoofinance

start_capital = 10000
shares = 18	# number of shares per order

class MyStrategy(strategy.BacktestingStrategy):
	def __init__(self, feed, instrument, smaPeriod):
		strategy.BacktestingStrategy.__init__(self, feed, start_capital)
		self.__position = None
		self.__instrument = instrument
		# We'll use adjusted close values instead of regular close values.
		self.setUseAdjustedValues(True)
		self.__sma = ma.SMA(feed[instrument].getPriceDataSeries(), smaPeriod)

	def onEnterOk(self, position):
		execInfo = position.getEntryOrder().getExecutionInfo()
		self.info("BUY at $%.2f" % (execInfo.getPrice()))

	def onEnterCanceled(self, position):
		self.__position = None

	def onExitOk(self, position):
		execInfo = position.getExitOrder().getExecutionInfo()
		self.info("SELL at $%.2f" % (execInfo.getPrice()))
		self.__position = None

	def onExitCanceled(self, position):
		# If the exit was canceled, re-submit it.
		self.__position.exitMarket()

	def onBars(self, bars):
		# Wait for enough bars to be available to calculate a SMA.
		if self.__sma[-1] is None:
			return

		bar = bars[self.__instrument]
		# If a position was not opened, check if we should enter a long position.
		if self.__position is None:
			if bar.getPrice() > self.__sma[-1]:
				# Enter a buy market order for 10 shares. The order is good till canceled.
				self.__position = self.enterLong(self.__instrument, shares, True)
		# Check if we have to exit the position.
		elif bar.getPrice() < self.__sma[-1]:
			self.__position.exitMarket()
	


ticker = 'cat'
year = 2015
csv_dir = '/home/andrew/Desktop'
csv_file = 'cat-2015.csv'

def run_strategy(smaPeriod):
	# download a CSV file from yahoo finance
	yahoofinance.download_daily_bars(ticker, year, csv_file)	
	# Load the yahoo feed from the CSV file
	feed = yahoofeed.Feed()
	feed.addBarsFromCSV(ticker, csv_file)

	# Evaluate the strategy with the feed.
	myStrategy = MyStrategy(feed, ticker, smaPeriod)
	myStrategy.run()
	equity = myStrategy.getBroker().getEquity()
	
	print '\nStarting portfolio value: $%.2f' % start_capital
	print 'Final portfolio value: $%.2f' % equity
	print 'Difference: %.2f' % (equity - start_capital)

# parameter is simple moving average (SMA) time period
run_strategy(15)
