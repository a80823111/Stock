#台股策略
import trade

stocks = trade.get_valid_static_stock() 

#trade.MA_signal(stocks)

trade.KD_trend_signal(stocks)

trade.KD_passivation_signal(stocks)