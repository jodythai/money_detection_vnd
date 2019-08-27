from money_detection_vnd import money_detection_vnd


def test_fib() -> None:
    assert money_detection_vnd.fib(0) == 0
    assert money_detection_vnd.fib(1) == 1
    assert money_detection_vnd.fib(2) == 1
    assert money_detection_vnd.fib(3) == 2
    assert money_detection_vnd.fib(4) == 3
    assert money_detection_vnd.fib(5) == 5
    assert money_detection_vnd.fib(10) == 55
