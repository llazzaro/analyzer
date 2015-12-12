from analyzer.backtest.backtester import BackTester


def main(session, store, pubsub, security, strategy, start, end):
    """
        This thread will retrieve info from the
        store and it will broadcast it
        to all trading engines.
        Trading Center must ignore this
        since is not realtime

    """

    backtester = BackTester(session, store, pubsub, security, strategy, start, end)

    backtester.consume()


if __name__ == '__main__':
    main()
