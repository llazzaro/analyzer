from analyzer.trading_center import TradingCenter


def main(session, pubsub):
    trading_center = TradingCenter(session, pubsub)

    while True:
        trading_center.consume()


if __name__ == '__main__':
    main()
