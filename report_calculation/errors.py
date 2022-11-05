class NoSuchCryptoPair(Exception):
    code = 0
    reason = "no-such-cryto-pair"
    description = "Crypto Pair does not existe in exchage"
