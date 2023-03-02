import ccxt
import time
import telegram

highest=float(0) # 최고가
highest_temp = float(0)
lowest=float(30000000) # 최저가
lowest_temp = float(30000000)
k=0

#---코인 매수 매도 비율 변수
symbol0 =input("(종목, ex) DOGE/USDT)") # symbol0=코인
standard = 0.000958  # 기준 구간
profit_position = input('매도폭: ') # 매도 기준
throw_position=input('1,2,3 구간 통과 폭: ') #  1,2,3 번째 구간 비율
leverage1 =int(input('레버리지 입력: '))
input_rate= int(input('진입비율 입력: '))
#42줄 amount0 변경
token = '(본인 토큰)'
mc = '(본인 id 숫자)'
bot = telegram.Bot(token)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #기본 정보 셋팅
binance = ccxt.binance(config={
    'apiKey': '(본인 API)',
    'secret': '(개인키)',
    'enableRateLimit': True, 
    'options': {
        'defaultType': 'future'
    }
})
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#시장 정보 가져오기
markets = binance.load_markets()
symbol = symbol0
market = binance.market(symbol)
#레버리지 정보
binance.fapiPrivate_post_leverage({
    'symbol': market['id'],
    'leverage': leverage1
})
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

#지갑 잔고 불러오기
def My_wallet():
    time.sleep(1)
    balance_wallet = binance.fetch_balance()
    return float(balance_wallet['total']['USDT'])

#사용 잔고 불러오기
def My_wallet_used():
    time.sleep(1)
    balance_wallet = binance.fetch_balance()
    return float(balance_wallet['used']['USDT'])

def Open_coin():
    coin_ohlcv = binance.fetch_ohlcv(symbol0,'5m')
    return coin_ohlcv[498][1]

def Close_coin():
    coin_ohlcv = binance.fetch_ohlcv(symbol0,'5m')
    return coin_ohlcv[498][4]

#최고가 최저가 현재가 추적
def Trace():
    try:
        global highest
        global lowest

        time.sleep(1)
        Open_coin()
        Close_coin()
        #최고가 갱신
        if Close_coin() > highest:
            highest = float(Close_coin())
            print('1. 현재 최고가: ',highest)
            highest_temp = float(Close_coin())
            bot.sendMessage(mc, '1. 현재 최고가 ')
            bot.sendMessage(mc, text = highest)
        if Open_coin() > highest:
            highest = float(Open_coin())
            print('1. 현재 최고가: ',highest)
            highest_temp = float(Open_coin())
            bot.sendMessage(mc, '1. 현재 최고가')
            bot.sendMessage(mc, text = highest)
        #촤저가 갱신
        if Close_coin() < lowest:
            lowest = float(Close_coin())
            lowest_temp = float(Close_coin())
            print('1. 현재 최저가: ',lowest)
            bot.sendMessage(mc, '1. 현재 최저가: ')
            bot.sendMessage(mc, text = lowest)
        if Open_coin() < lowest:
            lowest = float(Open_coin())
            lowest_temp = float(Open_coin())
            print('1. 현재 최저가: ',lowest)
            bot.sendMessage(mc, '1. 현재 최저가: ')
            bot.sendMessage(mc, text = lowest)
    except:
        print('인터넷 끊김으로 인한 오류')
        bot.sendMessage(mc, '인터넷 끊김으로 인한 오류')
        input('이어서 시작하려면 아무키나 눌러주세요: ')
        bot.sendMessage(mc, '이어서 시작하려면 아무키나 눌러주세요: ')

def Coin_last():
    time.sleep(1)
    ticker = binance.fetch_ticker(symbol0)
    coin_last= float(ticker['last'])
    return coin_last

def First_pass():
    print('')
    bot.sendMessage(mc, '/')
    print('첫 구간 도달')
    bot.sendMessage(mc, '첫 구간 도달')
    print('')
    bot.sendMessage(mc, '/')

def Second_pass():
    print('')
    bot.sendMessage(mc, '/')
    print('두 번째 구간 도달')
    bot.sendMessage(mc, '두 번째 구간 도달')
    print('')
    bot.sendMessage(mc, '/')

def Third_pass():
    print('')
    bot.sendMessage(mc, '/')
    print('세 번재 구간 도달')
    bot.sendMessage(mc, '세 번재 구간 도달')
    print('')
    bot.sendMessage(mc, '/')

def Standard():
    print('기준폭 도달')
    bot.sendMessage(mc, '기준폭 도달')
    print('')
    bot.sendMessage(mc, '/')

def Short_declare():
    print('숏 준비 중')
    bot.sendMessage(mc, '숏 준비 중')
    print('')
    bot.sendMessage(mc, '/')

def Long_declare():
    print('롱 준비 중')
    bot.sendMessage(mc, '롱 준비 중')
    print('')
    bot.sendMessage(mc, '/')

#잔고 조회
bot.sendMessage(mc, '현재 선물 잔고를 알려드립니다.:')
print('현재 선물 잔고를 알려드립니다.:', end=' ')
print(My_wallet())
bot.sendMessage(mc, My_wallet())

#주문량
amount0=float(((My_wallet())*leverage1*float(input_rate))/(100*Coin_last()))
print('')
bot.sendMessage(mc, '/')
print('매매 시작')
bot.sendMessage(mc, '매매 시작')
print('')
bot.sendMessage(mc, '/')

#short---------------------------------------------------------
while True:
    Coin_last()
    Trace()
    if k==1:
        print('')
        print('매매 시작')
        bot.sendMessage(mc, '매매 시작')
        print('')
        bot.sendMessage(mc, '/')
        k=0
# 기준 폭 도달확인----------------------------------------------------------
    if ((highest - lowest)/2) < Close_coin() and highest - lowest > standard:
        Standard()
        Short_declare()
        print('')
        bot.sendMessage(mc, '/')
        highest=0
        lowest=300000
        while True:
            Trace()
            Coin_last()
# 첫번째 변화 관측----------------------------------------------------------      
            if lowest+throw_position < Close_coin():
                First_pass()
                highest=0
                lowest=300000
                while True:
                    Coin_last()
                    Trace()
# 두번째 변화 관측---------------------------------------------------------- 
                    if highest - throw_position > Close_coin(): 
                        Second_pass()
                        highest=0
                        lowest=300000
                        while True:
                            Coin_last()
                            Trace()
# 세번째 바닥---------------------------------------------------------- 
                            if highest - throw_position < Coin_last() and ((highest_temp - lowest_temp)/2) < Coin_last():
                                Third_pass()
                                Coin_last()
                                try:
                                    order = binance.create_market_sell_order(symbol=symbol0,amount='{}'.format(amount0),params = {'positionSide': 'SHORT'})    
                                    A=1
                                except:
                                    print('롱 진행 중 이네요')
                                    bot.sendMessage(mc, '롱 진행 중 이네요')
                                    print('')
                                    bot.sendMessage(mc, '/')
                                    print('계좌에 돈이 들어있고 다시 타점이 온다면 실행할게요')
                                    bot.sendMessage(mc, '계좌에 돈이 들어있고 다시 타점이 온다면 실행할게요')
                                    #기준폭 도달 확인-----------------------
                                    while True:
                                        time.sleep(1)
                                        wait = My_wallet_used()
                                        if wait < 1 :
                                            highest = 0
                                            lowest =300000000
                                            Trace()
                                            if ((highest - lowest)/2) < Coin_last() and highest - lowest > standard:
                                                Standard()
                                                highest=0
                                                lowest=300000
                                                while True:
                                                    Trace()
                                                    Coin_last()
                                    # 첫번째 변화 관측----------------------------------------------------------      
                                                    if lowest+throw_position < Close_coin():
                                                        First_pass()
                                                        highest=0
                                                        lowest=300000
                                                        while True:
                                                            Coin_last()
                                                            Trace()
                                    # 두번째 변화 관측---------------------------------------------------------- 
                                                            if highest - throw_position > Close_coin():    
                                                                Second_pass()
                                                                highest=0
                                                                lowest=300000
                                                                while True:
                                                                    Coin_last()
                                                                    Trace()
                                    # 세번째 바닥---------------------------------------------------------- 
                                                                    if highest-throw_position > Coin_last() and ((highest_temp - lowest_temp)/2) < Coin_last():
                                                                        Third_pass()
                                                                        Coin_last()  
                                                                        order = binance.create_market_sell_order(symbol=symbol0,amount='{}'.format(amount0),params = {'positionSide': 'SHORT'}) 
                                                                        A=1
                                                                    elif highest-throw_position > Coin_last() and ((highest_temp - lowest_temp)/2) > Coin_last():
                                                                        Third_pass()
                                                                        Coin_last()  
                                                                        order = binance.create_market_buy_order(symbol=symbol0,amount='{}'.format(amount0),params = {'positionSide': 'SHORT'})    
                                                                        A=0
                                position_price = Coin_last()
                                print('숏 매수')
                                bot.sendMessage(mc, '숏 매수')
                                print('')
                                bot.sendMessage(mc, '/')
                                print('매도 포인트 찾는 중')
                                bot.sendMessage(mc, '매도 포인트 찾는 중')
                                print('')
                                bot.sendMessage(mc, '/')
                                while True:
                                    Coin_last()
                                    if position_price - profit_position > Coin_last() and A == 1:
                                        order = binance.create_market_buy_order(symbol=symbol0,amount='{}'.format(amount0),params = {'positionSide': 'SHORT'})
                                        print('숏 매도')
                                        bot.sendMessage(mc, '숏 매도')
                                        print('')
                                        bot.sendMessage(mc, '/')
                                        Coin_last()
                                        highest=float(0)
                                        lowest=float(30000000)
                                        break
                                    elif position_price + throw_position  < Coin_last() and A == 1:
                                        order = binance.create_market_buy_order(symbol=symbol0,amount='{}'.format(amount0),params = {'positionSide': 'SHORT'})                                  
                                        print('숏 손절')
                                        bot.sendMessage(mc, '숏 손절')
                                        print('')
                                        bot.sendMessage(mc, '/')
                                        Coin_last()
                                        highest=float(0)
                                        lowest=float(30000000)                                
                                        break
                                    elif position_price + profit_position < Coin_last() and A == 0:
                                        order = binance.create_market_sell_order(symbol=symbol0,amount='{}'.format(amount0),params = {'positionSide': 'SHORT'})
                                        print('롱 매도')
                                        bot.sendMessage(mc, '롱 매도')
                                        print('')
                                        bot.sendMessage(mc,  '/')
                                        Coin_last()
                                        highest=float(0)
                                        lowest=float(30000000)
                                        break
                                    elif position_price - throw_position  < Coin_last() and A == 0:
                                        order = binance.create_market_sell_order(symbol=symbol0,amount='{}'.format(amount0),params = {'positionSide': 'SHORT'})   
                                        print('롱 손절')
                                        bot.sendMessage(mc, '롱 손절')
                                        print('')
                                        bot.sendMessage(mc,  '/')
                                        Coin_last()
                                        highest=float(0)
                                        lowest=float(30000000)
                                        break
                                break
                            elif highest-throw_position > Coin_last() and ((highest_temp - lowest_temp)/2) > Coin_last():
                                Third_pass()
                                Coin_last()
                                try:
                                    order = binance.create_market_buy_order(symbol=symbol0,amount='{}'.format(amount0),params = {'positionSide': 'SHORT'})    
                                    A=0
                                except:
                                    print('롱 진행 중 이네요')
                                    bot.sendMessage(mc, '롱 진행 중 이네요')
                                    print('')
                                    bot.sendMessage(mc, ' ')
                                    print('계좌에 돈이 들어있고 다시 타점이 온다면 실행할게요')
                                    bot.sendMessage(mc, '계좌에 돈이 들어있고 다시 타점이 온다면 실행할게요')
                                    #기준폭 도달 확인-----------------------
                                    while True:
                                        time.sleep(1)
                                        wait = My_wallet_used()
                                        if wait < 1 :
                                            highest = 0
                                            lowest =300000000
                                            Trace()
                                            if ((highest - lowest)/2) < Coin_last() and highest - lowest > standard:
                                                Standard()
                                                highest =0
                                                lowest =300000
                                                while True:
                                                    Trace()
                                                    Coin_last()
                                        # 첫번째 변화 관측----------------------------------------------------------      
                                                    if lowest+throw_position < Close_coin():
                                                        First_pass()
                                                        highest=0
                                                        lowest=300000
                                                        while True:
                                                            Coin_last()
                                                            Trace()
                                        # 두번째 변화 관측---------------------------------------------------------- 
                                                            if highest - throw_position > Close_coin():    
                                                                Second_pass()
                                                                highest=0
                                                                lowest=300000
                                                                while True:
                                                                    Coin_last()
                                                                    Trace()
                                        # 세번째 바닥---------------------------------------------------------- 
                                                                    if highest-throw_position > Coin_last() and ((highest_temp - lowest_temp)/2) < Coin_last():
                                                                        Third_pass()
                                                                        Coin_last()  
                                                                        order = binance.create_market_sell_order(symbol=symbol0,amount='{}'.format(amount0),params = {'positionSide': 'SHORT'}) 
                                                                        A=1
                                                                    elif highest-throw_position > Coin_last() and ((highest_temp - lowest_temp)/2) > Coin_last():
                                                                        Third_pass()
                                                                        Coin_last()  
                                                                        order = binance.create_market_buy_order(symbol=symbol0,amount='{}'.format(amount0),params = {'positionSide': 'SHORT'})    
                                                                        A=0
                                position_price = Coin_last()
                                print('숏 매수')
                                bot.sendMessage(mc, '숏 매수')
                                print('')
                                bot.sendMessage(mc, '/')
                                print('매도 포인트 찾는 중')
                                bot.sendMessage(mc, '매도 포인트 찾는 중')
                                print('')
                                bot.sendMessage(mc, '/')
                                while True:
                                    Coin_last()
                                    if position_price - profit_position > Coin_last() and A == 1:
                                        order = binance.create_market_buy_order(symbol=symbol0,amount='{}'.format(amount0),params = {'positionSide': 'SHORT'})
                                        print('숏 매도')
                                        bot.sendMessage(mc, '숏 매도')
                                        print('')
                                        bot.sendMessage(mc, '/')
                                        Coin_last()
                                        highest=float(0)
                                        lowest=float(30000000)
                                        break
                                    elif position_price + throw_position  < Coin_last() and A == 1:
                                        order = binance.create_market_buy_order(symbol=symbol0,amount='{}'.format(amount0),params = {'positionSide': 'SHORT'})                                  
                                        print('숏 손절')
                                        bot.sendMessage(mc, '숏 손절')
                                        print('')
                                        bot.sendMessage(mc, '/')
                                        Coin_last()
                                        highest=float(0)
                                        lowest=float(30000000)                                
                                        break
                                    elif position_price + profit_position < Coin_last() and A == 0:
                                        order = binance.create_market_sell_order(symbol=symbol0,amount='{}'.format(amount0),params = {'positionSide': 'SHORT'})
                                        print('롱 매도')
                                        bot.sendMessage(mc, '롱 매도')
                                        print('')
                                        bot.sendMessage(mc,  '/')
                                        Coin_last()
                                        highest=float(0)
                                        lowest=float(30000000)
                                        break
                                    elif position_price - throw_position  > Coin_last() and A == 0:
                                        order = binance.create_market_sell_order(symbol=symbol0,amount='{}'.format(amount0),params = {'positionSide': 'SHORT'})   
                                        print('롱 손절')
                                        bot.sendMessage(mc, '롱 손절')
                                        print('')
                                        bot.sendMessage(mc,  '/')
                                        Coin_last()
                                        highest=float(0)
                                        lowest=float(30000000)
                                        break
                                break
                        break 
                break
        k=1
        continue   